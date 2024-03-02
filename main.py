from pydub import AudioSegment,effects
import noisereduce as nr
import numpy as np
import sys
import argparse


def sample_to_audio(samples, frame_rate, channels):
    """numpy配列をAudioSegmentオブジェクトに変換する"""
    if channels == 2:
        samples = np.ravel(samples)
    audio = AudioSegment(samples.tobytes(), frame_rate=frame_rate, sample_width=2, channels=channels)
    return audio


def audio_to_sample(audio):
    """AudioSegmentオブジェクトをnumpy配列に変換する"""
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = np.reshape(samples, (-1, 2))
    return samples


def reduce_noise(audio):
    """noisereduceを使用してノイズリダクションを適用する"""
    samples = audio_to_sample(audio)
    recuded_noise = nr.reduce_noise(y=samples, sr=audio.frame_rate)
    return sample_to_audio(recuded_noise, audio.frame_rate, 1)


def main():
    parser = argparse.ArgumentParser(description='Podcastの音声の前処理をやるやつ')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('--noizereduction', action='store_true', help="ノイズ除去をするかどうか")
    args = parser.parse_args()


    # オーディオを読み込む
    audio = AudioSegment.from_file(args.input_file, format="mp3")


    if args.noizereduction:
        ## ノイズ除去フィルター
        print("Noise reduction")
        audio = reduce_noise(audio)
    ## 大きい音と小さい音をコンプレッション
    print("Dynamic compressor")
    audio = effects.compress_dynamic_range(audio, threshold=-10, ratio=12.0, attack=5.0, release=100)
    ## normalize
    print("Normalize")
    audio = effects.normalize(audio)

    # 処理後のオーディオを保存
    audio.export(args.output_file, format="mp3")

if __name__ == "__main__":
    main()
