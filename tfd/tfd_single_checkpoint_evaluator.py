import argparse
import glob
import os
import sys

import numpy

from anna.datasets.supervised_data_loader import SupervisedDataLoader
from anna import util

import data_paths
from model import SupervisedModel


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='tfd_single_checkpoint_evaluator',
        description='Script to evaluate single checkpoint on TFD.')
    parser.add_argument("-s", "--split", default='0',
                        help='Training split of TFD to use. (0-4)')
    parser.add_argument("checkpoint_file",
                        help='Path to single model checkpoint (.pkl) file.')
    args = parser.parse_args()

    checkpoint_file = args.checkpoint_file
    fold = int(args.split)
    dataset_path = os.path.join(data_paths.tfd_data_path, 'npy_files/TFD_96/split_'+str(fold))

    print 'Checkpoint: %s' % checkpoint_file
    print 'Testing on split %d\n' % fold

    # Load model
    model = SupervisedModel('evaluation', './')

    # Load dataset
    supervised_data_loader = SupervisedDataLoader(dataset_path)
    test_data_container = supervised_data_loader.load(2)
    test_data_container.X = numpy.float32(test_data_container.X)
    test_data_container.X /= 255.0
    test_data_container.X *= 2.0

    # Construct evaluator
    preprocessor = [util.Normer3(filter_size=5, num_channels=1)]

    evaluator = util.Evaluator(model, test_data_container,
                               checkpoint_file, preprocessor)

    # For the inputted checkpoint, compute the overall test accuracy
    accuracies = []
    print 'Checkpoint: %s' % os.path.split(checkpoint_file)[1]
    evaluator.set_checkpoint(checkpoint_file)
    accuracy = evaluator.run()
    print 'Accuracy: %f\n' % accuracy
    accuracies.append(accuracy)
