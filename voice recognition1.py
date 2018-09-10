from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

import tensorflow as tf
import pyaudio
import wave
# pylint: disable=unused-import
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
# pylint: enable=unused-import

FLAGS = None
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512 
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"
TXT_OUTPUT_FILENAME = "test.txt"



def load_graph(filename):
    """Unpersists graph from file as default graph."""
    with tf.gfile.FastGFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


def load_labels(filename):
  """Read in labels, one label per line."""
  return [line.rstrip() for line in tf.gfile.GFile(filename)]


def run_graph(wav_data, labels, input_layer_name, output_layer_name,
              num_top_predictions):
  """Runs the audio data through the graph and prints predictions."""
  with tf.Session() as sess:
    # Feed the audio data as input to the graph.
    #   predictions  will contain a two-dimensional array, where one
    #   dimension represents the input image count, and the other has
    #   predictions per class
    softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
    predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})

    # Sort to show labels in order of confidence
    top_k = predictions.argsort()[-num_top_predictions:][::-1]
    for node_id in top_k:
      human_string = labels[node_id]
      score = predictions[node_id]
      print('%s (score = %.5f)' % (human_string, score))
      f = open("text.txt",'w')
      f.write('%s' % (human_string))
      f.close()
      # save to a file ('%s (score = %.5f)' % (human_string, score)

    return 0


def label_wav(wav, labels, graph, input_name, output_name, how_many_labels):
    """Loads the model and labels, and runs the inference to print predictions."""
    if not wav or not tf.gfile.Exists(wav):
        tf.logging.fatal('Audio file does not exist %s', wav)

    if not labels or not tf.gfile.Exists(labels):
        tf.logging.fatal('Labels file does not exist %s', labels)

    if not graph or not tf.gfile.Exists(graph):
        tf.logging.fatal('Graph file does not exist %s', graph)

    labels_list = load_labels(labels)

    # load graph, which is stored in the default session
    load_graph(graph)

    # start Recording
    print ('recording...')
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK)
      frames.append(data)
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    audio.terminate()
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    print ('finished recording')
  
    with open(wav, 'rb') as wav_file:
        wav_data = wav_file.read()
    run_graph(wav_data, labels_list, input_name, output_name, how_many_labels)
    
    


def main(_):
  """Entry point for script, converts flags to arguments."""
  label_wav(FLAGS.wav, FLAGS.labels, FLAGS.graph, FLAGS.input_name,
            FLAGS.output_name, FLAGS.how_many_labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
      '--wav', type=str, default='file.wav', help='Audio file to be identified.')
    parser.add_argument(
      '--graph', type=str, default='my_frozen_graph.pb', help='Model to use for identification.')
    parser.add_argument(
      '--labels', type=str, default='speech_commands_train/conv_labels.txt', help='Path to file containing labels.')
    parser.add_argument(
      '--input_name',
      type=str,
      default='wav_data:0',
      help='Name of WAVE data input node in model.')
    parser.add_argument(
      '--output_name',
      type=str,
      default='labels_softmax:0',
      help='Name of node outputting a prediction in the model.')
    parser.add_argument(
      '--how_many_labels',
      type=int,
      default=1,
      help='Number of results to show.')

    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
f = open("text.txt",'w')
line = f.readline()
f.close()

pinMode(7,OUTPUT)
     
if line == "up":
    digitalWrite(7,HIGH);
                
if line == "down":
    digitalWrite(7,LOW);



    