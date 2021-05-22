# generative_image_creation

## Usage

1. Clone this repository

```bash
git clone https://github.com/yanliang789/generative_image_creation.git
cd generative_image_creation/
```

2. Software installation:
   ### Install the dependencies:

```bash
conda create -n generate_image python=3.6.7
conda activate generate_image
pip install munch
pip install torch
pip install image
pip install torchvision
pip install opencv-python
pip install scikit-image
pip install tqdm
pip install ffmpeg
pip install Flask
```

3. Active virtual environment: whenever you want to run the project

```bash
conda activate generate_image
```

4. Datasets and pre-trained networks

### Datasets and pre-trained networks

A script to download datasets used in StarGAN v2 and the corresponding pre-trained networks. The datasets and network checkpoints will be downloaded and stored in the `data` and `expr/checkpoints` directories, respectively.

<b>CelebA-HQ.</b> To download the [CelebA-HQ](https://drive.google.com/drive/folders/0B4qLcYyJmiz0TXY1NG02bzZVRGs) dataset and the pre-trained network, run the following commands:

```bash
bash download.sh celeba-hq-dataset
bash download.sh pretrained-network-celeba-hq
bash download.sh wing
```

5. Start server

```bash
python app.py
```

6. use the following endpoints as need

There are 4 APIs:

- hom page: http://127.0.0.1:8080/
- upload sample: http://127.0.0.1:8080/add_sample
  There are some default sample hairstyle pictures as sample reference, add_sample is used for user update their own reference as need.
- upload source: http://127.0.0.1:8080/add_src
  Use for upload user's own picture to generate new hairstyle.
- genneate hairstyle: http://127.0.0.1:8080/style
  Once "style/" was called, then it will genearte the new hairstyle. It usually takes some time to generate, the more samples and source pictures used the more time need. At the end web will show the and save the generated images.

### Generating Image

After downloading the pre-trained networks, you can synthesize output images reflecting diverse styles (e.g., hairstyle) of reference images.
DataSet: I use <b>CelebA-HQ.</b> to generate images.

Before call the APIS, also can <b>transform</b> a custom image, first crop the image manually so that the proportion of face occupied in the whole is similar to that of CelebA-HQ. Then, run the following command for additional fine rotation and cropping. All custom images in the `inp_dir` directory will be aligned and stored in the `out_dir` directory.

### Tranform Image

```bash
python main.py --mode align \
               --inp_dir assets/representative/custom/female \
               --out_dir assets/representative/celeba_hq/src/female
```

## Evaluation metrics

To evaluats value run the following commands:

```bash
python main.py --mode eval --num_domains 2 --w_hpf 1 \
               --resume_iter 100000 \
               --train_img_dir data/celeba_hq/train \
               --val_img_dir data/celeba_hq/val \
               --checkpoint_dir expr/checkpoints/celeba_hq \
               --eval_dir expr/eval/celeba_hq
```

Note that the evaluation metrics are calculated using random latent vectors or reference images

| Dataset <img width=50/> | <img width=15/> FID (latent) <img width=15/> | <img width=10/> LPIPS (latent) <img width=10/> | <img width=5/> FID (reference) <img width=5/> | LPIPS (reference)  | <img width=10/> Elapsed time <img width=10/> |
| :---------------------- | :------------------------------------------: | :--------------------------------------------: | :-------------------------------------------: | :----------------: | :------------------------------------------: |
| `celeba-hq`             |               13.73 &pm; 0.06                |               0.4515 &pm; 0.0006               |                23.84 &pm; 0.03                | 0.3880 &pm; 0.0001 |                  49min 51s                   |

## Training networks(celeba-hq dataset)

I use pre-trained models which trained by StarGan v2
To train StarGAN v2 from scratch, run the following commands. Generated images and network checkpoints will be stored in the `expr/samples` and `expr/checkpoints` directories, respectively. Training takes about three days on a single Tesla V100 GPU. Please see [here](https://github.com/clovaai/stargan-v2/blob/master/main.py#L86-L179) for training arguments and a description of them.

```bash
python main.py --mode train --num_domains 2 --w_hpf 1 \
               --lambda_reg 1 --lambda_sty 1 --lambda_ds 1 --lambda_cyc 1 \
               --train_img_dir data/celeba_hq/train \
               --val_img_dir data/celeba_hq/val
```

## source

The source code, pre-trained models, and dataset are available under [Creative Commons BY-NC 4.0](https://github.com/clovaai/stargan-v2/blob/master/LICENSE) license by NAVER Corporation.
