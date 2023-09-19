from PIL import Image
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import traceback
import json

import torch.nn as nn

import textdistance
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

@csrf_exempt
def post_bank(request):
    if request.method == 'POST':
        # 클라이언트로부터 문자열 받기
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            user_input = request_data.get('voice_bank')
        except json.JSONDecodeError as e:
            # JSON 디코딩 오류 처리
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        print("client:", user_input)

        if user_input is not None:
            # 비교 대상 문자열 목록
            candidates = ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행", "토스뱅크", "카카오뱅크"]
            # "궁민은행"과 제일 비슷한 값을 찾음

            # 가장 가까운 문자열 찾기
            min_distance = float('inf')  # 최소 거리 초기화
            closest_candidate = None

            for candidate in candidates:
                distance = textdistance.levenshtein(user_input, candidate)
                if distance < min_distance:
                    min_distance = distance
                    closest_candidate = candidate

            print("return", closest_candidate)
            # 결과 리턴
            response_data = {
                "closest_bank": closest_candidate,
            }
            return JsonResponse(response_data)
        else:
            # 'user_input'이 None인 경우 처리
            return JsonResponse({"error": "User input is missing."}, status=400)

# POST 응답 처리
from pydub import AudioSegment
import torch
import torchvision.transforms as transforms
import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt
import matplotlib
import subprocess
import struct

matplotlib.use('Agg')

FIG_SIZE = (15, 10)
DATA_NUM = 30

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# 음성 데이터의 샘플링 레이트, 채널 수, 샘플링 포맷 등을 정의합니다.
SAMPLE_RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2

# 다음 세 줄을 추가하여 모델을 미리 로드합니다.
resnet = None
model_loaded = False
peekIndex = 0
image_url = ""

# 이전에 모델을 로드하는 함수를 정의합니다.
def load_resnet_model():
    global resnet
    global model_loaded
    if not model_loaded:
        resnet = torch.hub.load('pytorch/vision:v0.6.0', 'resnet34')
        resnet.fc = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(512, 10)
        )
        resnet.load_state_dict(torch.load('BankingServer/resnetModel/best_resnet34_weights(911).pth'))
        resnet.eval()
        model_loaded = True


# m4a -> wav -> spectrogram / -> resnetModel -> result
@csrf_exempt
def process_audio(request):
    global peekIndex, image_url

    print("process_audio")
    try:
        if request.method == 'POST':
            print("POST")

            load_resnet_model()

            # POST 요청에서 biteArray 데이터를 가져옵니다.
            requestBody = json.loads(request.body)  # 안드로이드 앱에서 보낸 데이터를 가져옵니다.
            byte_data = requestBody['recordData']
            byte_array = bytes([struct.pack('b', x)[0] for x in byte_data])

            with open('my_audio_file.aac', 'wb+') as destination:
                for i in range(0, len(byte_array), 32):
                    chunk = byte_array[i:i + 32]
                    destination.write(chunk)

            # aac -> wav
            input_file = "my_audio_file.aac"
            output_file = "my_audio_file.wav"

            # Run the ffmpeg command to convert the AAC file to WAV
            subprocess.run(["ffmpeg", "-y", "-i", input_file, output_file])

            audio1 = AudioSegment.from_file("my_audio_file.wav", format="wav")
            silence = AudioSegment.silent(duration=1000)  # 1초 묵음
            combined_audio = audio1 + silence

            # export the concatenated audio as a new file
            file_path = "combined.wav"
            combined_audio.export(file_path, format="wav")

            # 신호 및 샘플링 레이트 가져오기
            sig, sr = librosa.load(file_path, sr=22050)

            # 에너지 평균 구하기
            sum = 0
            for i in range(0, sig.shape[0]):
                sum += sig[i] ** 2
            mean = sum / sig.shape[0]

            # 피크인덱스 찾기
            for i in range(0, sig.shape[0]):
                if (sig[i] ** 2 >= mean):
                    peekIndex = i
                    break
            #
            START_LEN = 1102
            END_LEN = 20948
            if peekIndex > 1102:
                startPoint = peekIndex - START_LEN
                endPoint = peekIndex + 22050
            else:
                startPoint = peekIndex
                endPoint = peekIndex + END_LEN

            # 단순 푸리에 변환 -> Specturm
            fft = np.fft.fft(sig[startPoint:endPoint])

            # 복소공간 값 절댓갑 취해서, magnitude 구하기
            magnitude = np.abs(fft)

            # Frequency 값 만들기
            f = np.linspace(0, sr, len(magnitude))

            # 푸리에 변환을 통과한 specturm은 대칭구조로 나와서 high frequency 부분 절반을 날려고 앞쪽 절반만 사용한다.
            left_spectrum = magnitude[:int(len(magnitude) / 2)]
            left_f = f[:int(len(magnitude) / 2)]

            # STFT -> Spectrogram
            hop_length = 512  # 전체 frame 수
            n_fft = 2048  # frame 하나당 sample 수

            # calculate duration hop length and window in seconds
            hop_length_duration = float(hop_length) / sr
            n_fft_duration = float(n_fft) / sr

            # STFT
            stft = librosa.stft(sig[startPoint:endPoint], n_fft=n_fft, hop_length=hop_length)

            # 복소공간 값 절댓값 취하기
            magnitude = np.abs(stft)

            # magnitude > Decibels
            log_spectrogram = librosa.amplitude_to_db(magnitude)

            FIG_SIZE = (10, 10)

            # display spectrogram
            plt.figure(figsize=FIG_SIZE)
            librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length, cmap='magma')

            # matplotlib 라이브러리를 사용하여 생성된 spectrogram 이미지를 jpg 형식으로 저장
            image_path = 'static/images/' + 'test.jpg'
            plt.savefig(image_path)

            plt.close()


#             resnet = torch.hub.load('pytorch/vision:v0.6.0', 'resnet34')
#             resnet.fc = nn.Sequential(
#                 nn.Dropout(p=0.5),  # 드롭아웃 추가
#                 nn.Linear(512, 10)  # 출력층의 뉴런 수는 10
# )
#             # 모델 입히기
#             resnet.load_state_dict(torch.load('BankingServer/resnetModel/best_resnet34_weights(911).pth'))
#             # switch resnetModel to evaluation mode
#             resnet.eval()
            # define the image transforms
            image_transforms = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])

            # 이미지 열기
            image = Image.open(image_path)

            # apply the transforms to the test image
            test_image_tensor = image_transforms(image)
            # add batch dimension to the image tensor
            test_image_tensor = test_image_tensor.unsqueeze(0)

            # get the resnetModel's prediction
            with torch.no_grad():
                prediction = resnet(test_image_tensor)

            # get the predicted class index
            predicted_class_index = torch.argmax(prediction).item()

            response = {'predicted_number': number[predicted_class_index]}
            # 예측값 알파벳 출력
            print("post: ", response)
            return JsonResponse(response)
    except Exception as e:
        print(traceback.format_exc())  # 예외 발생시 traceback 메시지 출력
        return HttpResponseServerError()  # 500 Internal Server Error 응답 반환

