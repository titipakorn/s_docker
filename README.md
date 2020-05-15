# Computer Vision Utilities

THIS IS FOR TESTING ONLY\

[PREPARING DATA]\

docker run --rm -it --init \
 --runtime=nvidia \
 --ipc=host \
 --volume="/data1/CIM/INPUT/device:/app/data/device" \
 --volume="/data1/CIM/INPUT/app:/app/data/app" \
 --volume="/data1/CIM/INPUT/app/crop:/app/similarity_data/" \
 --volume="/data1/CIM/INPUT/classify:/app/classifier_data" \
 signature /bin/bash

source activate cv

conda install opencv -y

python duplicate_images.py [DESIRE AMOUNT] --path [DESIRE DESTINATION], example: python duplicate_images.py 24 /app/data/app/crop/,

python extract_signature.py, PATH: /app/data/device and /app/data/app

python prepare_data.py, PATH: /app/data/device and /app/data/app, only use for preparing data training of similarity model

[TRAINING CLASSIFIER]\

1.Extract signature from PDF files by running python extract_signature.py from [PREPARING DATA] \
2.Copy jpeg files from /app/data/app/crop and /app/data/device/crop \
3.Create a folder for each class, for example, No_Signature and Signature \
4.Copy jpeg files of that class into that folder \
5.Copy all folders to /data1/CIM/INPUT/classify \
6.run: python train_classifier.py\
7.after training finished, copy the model out of the docker by using this command\
cp /app/classifier_model.pkl /app/classifier_data/
8.using WINSCP to copy the model from /data1/CIM/INPUT/classify\

[TRAINING SIMILARITY]\
0.run: chmod +x /app/move_file2folder.bash && chmod +x /app/mvaug.bash\
1.Extract signature from PDF files by running python extract_signature.py from [PREPARING DATA]\
2.run: cd /app/data/app/crop\
3.run: /app/move_file2folder.bash\
4.run: python /app/duplicate_images.py 24 --path /app/data/app/crop/
COPY FOLDERS for train(70%) and test (30%)
6.run: python /app/train_similarity.py\
7.after training finished, copy the model out of the docker by using this command\
cp /app/similarity_model.pkl /app/classifier_data/
8.using WINSCP to copy the model from /data1/CIM/INPUT/classify

[API SERVICE][https://github.com/titipakorn/sig_test_api]\
#Running the service\
docker run --rm -it -p 6666:6666 --init \
 --runtime=nvidia \
 --ipc=host \
 --volume="/data1/CIM/Test_API/:/app/api/" \
 --volume="/data1/CIM/models/signature/:/app/models/" \
 test_api_signature /bin/bash

1.copy model files to /data1/CIM/models/signature/
2.edit config.py to fit your need\
3.copy files from GITHUB downloaded files to /data1/CIM/Test_API/
4.running the docker with the above command\
5.run: cp -r api/\* .\
6.run: source activate cv\
7.run: uvicorn main:app --port 6666 --host 0.0.0.0\

#Testing the service

[CLASSIFY TESTING]\
1.copy signature images to '/data1/CIM/Test_API/check/'\
2.run: source /data1/anaconda3/bin/activate\
3.run: python /data1/CIM/Test_API/evaluation_check.py\
4.download check_signature.csv from /data1/CIM/Test_API/ to see the results\

[SIMILARITY TESTING]\
1.copy signature images to '/data1/CIM/Test_API/compare/app/' and '/data1/CIM/Test_API/compare/device/'\
2.run: source /data1/anaconda3/bin/activate\
3.run: python /data1/CIM/Test_API/evaluation_compare.py\
4.download compare_result_signature.csv from /data1/CIM/Test_API/ to see the results\

[APPENDIX]\

almight command:\
sudo -u root [CMD]\
for example, sudo -u root chown -R user /app/

edit ~/.bashrc

echo "export LC_ALL=C.UTF-8" >> ~/.bashrc\
echo "export LANG=C.UTF-8" >> ~/.bashrc\

mkdir -p /.cache/torch/checkpoints/

for train classify\
cp /app/classifier_data/resnet18-5c106cde.pth ~/.cache/torch/checkpoints/

for train similarity\
cp /app/classifier_data/resnet50-19c8e357.pth ~/.cache/torch/checkpoints/

[DOWNLOAD AND COPY TO /data1/CIM/INPUT/classify]\

https://download.pytorch.org/models/resnet18-5c106cde.pth

https://download.pytorch.org/models/resnet50-19c8e357.pth

[DOCKER UPDATE TO NEW IMAGE]

docker ps\
[find the current container ID]

docker commit CONTAINER_ID image_name:TAG

#signature in the docker command is the image_name
