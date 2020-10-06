%%%%% FIT GLM TYPE 3 [single-trial, fit HRF. idea is to choose the best R2 for each voxel.] [EXPENSIVE WRT DISK SPACE AND TIME]
% load in the hrfs
load(hrfmanifoldfile,'hrfs');  % TR x different-hrfs
% approach: single-trial analysis, systematically try different HRFs, no boots
% calc
nx = size(data{1},1)
ny = size(data{1},2)
nz = size(data{1},3)
nh = size(hrfs,2)
nr = length(data)
nb = size(stimulus{1},2)
% initialize
FitHRFR2 =    zeros(nx,ny,nz,nh,'single');     % X x Y x Z x HRFs with R2 values (all runs)
FitHRFR2run = zeros(nx,ny,nz,nr,nh,'single');  % X x Y x Z x 12 runs x HRFs with R2 separated by runs
modelmd =     zeros(nx,ny,nz,nb,'single');     % X x Y x Z x trialbetas
% figure out chunking scheme
totalnum = prod(sizefull(data{1},3));
numvoxchunk = 200000;
chunks = chunking(1:size(data{1},3),ceil(size(data{1},3)/ceil(totalnum/numvoxchunk)))
% loop over chunks
for z=1:length(chunks), z
  % do the fitting and accumulate all the betas
  modelmd0 = zeros(nx,ny,length(chunks{z}),nb,nh,'single');  % X x Y x someZ x trialbetas x HRFs
  for p=1:size(hrfs,2)
    tic; results = GLMestimatemodel(stimulus,cellfun(@(x) x(:,:,chunks{z},:),data,'UniformOutput',0),stimdur,tr,'assume',hrfs(:,p),0); toc;
    FitHRFR2(:,:,chunks{z},p) = results.R2;
    FitHRFR2run(:,:,chunks{z},:,p) = results.R2run;
    modelmd0(:,:,:,:,p) = results.modelmd{2};
    clear results;
  end
  % keep only the betas we want
  tic;
  [~,ii] = max(FitHRFR2(:,:,chunks{z},:),[],4);
  modelmd(:,:,chunks{z},:) = matrixindex(modelmd0,repmat(ii,[1 1 1 size(modelmd0,4)]),5);
  clear modelmd0;
  toc;
end
% use R2 to select the best HRF for each voxel
[R2,HRFindex] = max(FitHRFR2,[],4);  % HRFindex is X x Y x Z
% also, use R2 from each run to select best HRF
[~,HRFindexrun] = max(FitHRFR2run,[],5);
% using each voxel's best HRF, what are the corresponding R2run values?
R2run = matrixindex(FitHRFR2run,repmat(HRFindex,[1 1 1 size(FitHRFR2run,4)]),5);  % R2run is X x Y x Z x 12 runs
% save
tic;
save(sprintf('%s/GLMdenoise_nsdBASICsingletrialfithrf.mat',glmdir), ...
  'FitHRFR2','FitHRFR2run','HRFindex','HRFindexrun','R2','R2run','modelmd','-v7.3');
toc;