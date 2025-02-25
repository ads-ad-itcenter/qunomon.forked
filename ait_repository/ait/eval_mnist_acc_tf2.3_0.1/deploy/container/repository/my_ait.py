#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook
# 
# 
# ## notebook of structure
# 
# |#|area name|cell num|description|edit or not|
# |---|---|---|---|---|
# | 1|flags set|1|setting of launch jupyter or ait flag.|no edit|
# | 2|ait-sdk install|1|Use only jupyter launch.<br>find ait-sdk and install.|no edit|
# | 3|create requirements and pip install|3|Use only jupyter launch.<br>create requirements.txt.<br>And install by requirements.txt.|should edit(second cell, you set use modules.)|
# | 4|import|2|you should write use import modules.<br>but bottom lines do not edit.|should edit(first cell, you import your moduel.)|
# | 5|create manifest|1|Use only jupyter launch.<br>create ait.manifest.json.|should edit|
# | 6|create input|1|Use only jupyter launch.<br>create ait.input.json.|should edit|
# | 7|initialize|1|this cell is initialize for ait progress.|no edit|
# | 8|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
# | 9|main|1|Read the data set or model and calls the function defined in `functions-area`.|should edit|
# |10|entrypoint|1|Call the main function.|no edit|
# |11|license attribute set|1|Use only notebook launch.<br>Setting attribute for license.|should edit|
# |12|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and create dag.py.|no edit|
# 
# ## notebook template revision history
# 
# ### 1.0.1 2020/10/21
# 
# * add revision history
# * separate `create requirements and pip install` editable and noeditable
# * separate `import` editable and noeditable
# 
# ### 1.0.0 2020/10/12
# 
# * new cerarion

# In[ ]:


#########################################
# area:flags set
# do not edit
#########################################

# Determine whether to start AIT or jupyter by startup argument
import sys
is_ait_launch = (len(sys.argv) == 2)


# In[2]:


#########################################
# area:ait-sdk install
# do not edit
#########################################
if not is_ait_launch:
    # get ait-sdk file name
    from pathlib import Path
    from glob import glob
    import re

    def numericalSort(value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    latest_sdk_file_path=sorted(glob('../lib/*.whl'), key=numericalSort)[-1]

    ait_sdk_name = Path(latest_sdk_file_path).name
    
    # copy to develop dir
    import shutil
    current_dir = get_ipython().run_line_magic('pwd', '')
    shutil.copyfile(f'../lib/{ait_sdk_name}', f'{current_dir}/{ait_sdk_name}')

    # install ait-sdk
    get_ipython().system('pip install --upgrade pip')
    get_ipython().system('pip install --force-reinstall ./$ait_sdk_name')


# In[3]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()


# In[4]:


#########################################
# area:create requirements and pip install
# should edit
#########################################
if not is_ait_launch:
    requirements_generator._package_list = []
    requirements_generator.add_package('matplotlib', '3.3.0')
    requirements_generator.add_package('numpy', '1.19.2')
    requirements_generator.add_package('pandas', '1.1.0')
    requirements_generator.add_package('scikit-learn', '0.23.2')
    requirements_generator.add_package('scipy', '1.4.1')
    requirements_generator.add_package('seaborn', '0.10.1')
    requirements_generator.add_package('sklearn', '0.0')
    requirements_generator.add_package('tensorflow', '2.5.0')
    requirements_generator.add_package('tensorflow-estimator', '2.5.0')


# In[5]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[6]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
from typing import List
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, roc_curve, auc, roc_auc_score
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import interp
from itertools import cycle
from os import makedirs, path

from ait_sdk.utils import get_summary_text
from ait_sdk.utils.mnist import MNIST

# must use modules
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[ ]:


#########################################
# area:import
# do not edit
#########################################

# must use modules
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[ ]:


#########################################
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('eval_mnist_acc_tf2.3')
    manifest_genenerator.set_ait_description('Only Sequential API Model\n\n<QualityMeasurement>\nAccuracy=TP+TNTP+FP+FN+TN\nPrecision=TPTP+FP\nRecall=TPTP+FN\nF−measure=2Recall∗PrecisionRecall+Precision\nAUC\n\n<Resources>\nROC曲線\n混同行列\nNG予測画像')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Accuracy_of_trained_model')
    manifest_genenerator.set_ait_reference('')

    manifest_genenerator.add_ait_inventories(name='trained_model', 
                                             type_='model', 
                                             description='Tensorflow 2.3で学習したモデル', 
                                             format_=['h5'], 
                                             schema='https://support.hdfgroup.org/HDF5/doc/')
    manifest_genenerator.add_ait_inventories(name='test_set_images', 
                                            type_='dataset', 
                                            description='テスト画像セット（MNISTフォーマット）', 
                                            format_=['gz'], 
                                            schema='http://yann.lecun.com/exdb/mnist/')
    manifest_genenerator.add_ait_inventories(name='test_set_labels', 
                                            type_='dataset', 
                                            description='テスト画像ラベル（MNISTフォーマット）', 
                                            format_=['gz'], 
                                            schema='http://yann.lecun.com/exdb/mnist/')
    
    manifest_genenerator.add_ait_parameters(name='class_count', 
                                            type_='int', 
                                            description='multiple classification class number', 
                                            default_val='10',
                                            min_value='2',
                                            max_value='99')
    manifest_genenerator.add_ait_parameters(name='auc_average', 
                                            type_='string', 
                                            description='{‘micro’, ‘macro’, ‘samples’, ‘weighted’}\r\nref:\r\nhttps://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html', 
                                            default_val='macro')
    manifest_genenerator.add_ait_parameters(name='auc_multi_class', 
                                            type_='string', 
                                            description='{‘raise’, ‘ovr’, ‘ovo’}\nref:\nhttps://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html', 
                                            default_val='raise')

    manifest_genenerator.add_ait_measures(name='Accuracy', 
                                          type_='float', 
                                          description='(TP+TN) / (TP+FP+FN+TN)', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='Precision', 
                                          type_='float', 
                                          description='TP / (TP+FP)', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='Recall', 
                                          type_='float', 
                                          description='TP / (TP+FN)', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='F−measure', 
                                          type_='float', 
                                          description='(2Recall∗Precision) / (Recall+Precision)', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='AUC', 
                                          type_='float', 
                                          description='Area under the ROC curve', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='AccuracyByClass', 
                                          type_='float', 
                                          description='Accuracy for each class.', 
                                          structure='sequence',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='PrecisionByClass', 
                                          type_='float', 
                                          description='Precision for each class.', 
                                          structure='sequence',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='RecallByClass', 
                                          type_='float', 
                                          description='Recall for each class.', 
                                          structure='sequence',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='F−measureByClass', 
                                          type_='float', 
                                          description='F−measure for each class.', 
                                          structure='sequence',
                                          min='0',
                                          max='1')

    manifest_genenerator.add_ait_resources(name='ConfusionMatrixHeatmap', 
                                           type_='picture', 
                                           description='混同行列(ヒートマップ)')
    manifest_genenerator.add_ait_resources(name='ROC-curve', 
                                           type_='picture', 
                                           description='ROC曲線')
    manifest_genenerator.add_ait_resources(name='NGPredictImages', 
                                           type_='picture', 
                                           description='推論NGとなった画像の一覧を、正解ラベルの枚数分だけ出力する')

    manifest_genenerator.add_ait_downloads(name='Log', 
                                           description='AIT実行ログ')
    manifest_genenerator.add_ait_downloads(name='ConfusionMatrixCSV', 
                                           description='混同行列')
    manifest_genenerator.add_ait_downloads(name='PredictionResult', 
                                           description='ID,正解ラベル,推論結果確率(ラベル毎)')

    manifest_path = manifest_genenerator.write()


# In[ ]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories(name='trained_model',
                                        value='trained_model/model_1.h5')
    input_generator.add_ait_inventories(name='test_set_images',
                                        value='test_set_images/t10k-images-idx3-ubyte.gz')
    input_generator.add_ait_inventories(name='test_set_labels',
                                        value='test_set_labels/t10k-labels-idx1-ubyte.gz')

    input_generator.set_ait_params(name='class_count',
                                   value='10')
    input_generator.set_ait_params(name='auc_average',
                                   value='macro')
    input_generator.set_ait_params(name='auc_multi_class',
                                   value='raise')

    input_generator.write()


# In[ ]:


#########################################
# area:initialize
# do not edit
#########################################

logger = get_logger()

ait_manifest = AITManifest()
ait_input = AITInput(ait_manifest)
ait_output = AITOutput(ait_manifest)

if is_ait_launch:
    # launch from AIT
    current_dir = path.dirname(path.abspath(__file__))
    path_helper = AITPathHelper(argv=sys.argv, ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)
else:
    # launch from jupyter notebook
    # ait.input.json make in input_dir
    input_dir = '/usr/local/qai/mnt/ip/job_args/1/1'
    current_dir = get_ipython().run_line_magic('pwd', '')
    path_helper = AITPathHelper(argv=['', input_dir], ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)

ait_input.read_json(path_helper.get_input_file_path())
ait_manifest.read_json(path_helper.get_manifest_file_path())

### do not edit cell


# In[ ]:


class ACCCalculator:
    """
    精度を計算する

    accuracy calculator
    """

    def normalize_y_pred(self, y_pred):
        return K.one_hot(K.argmax(y_pred), y_pred.shape[-1])

    def class_true_positive(self, class_label, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.cast(K.equal(y_true[:, class_label] + y_pred[:, class_label], 2),
                    K.floatx())

    def class_precision(self, class_label, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.sum(self.class_true_positive(class_label, y_true, y_pred)) / (K.sum(y_pred[:, class_label]) + K.epsilon())

    def all_class_precision(self, y_true, y_pred):
        return [self.class_precision(i, y_true, y_pred) for i in range(y_pred.shape[-1])]

    def macro_precision(self, y_true, y_pred):
        class_count = y_pred.shape[-1]
        return K.sum([self.class_precision(i, y_true, y_pred) for i in range(class_count)])             / K.cast(class_count, K.floatx())

    def class_recall(self, class_label, y_true, y_pred):
        return K.sum(self.class_true_positive(class_label, y_true, y_pred)) / (K.sum(y_true[:, class_label]) + K.epsilon())

    def all_class_recall(self, y_true, y_pred):
        return [self.class_recall(i, y_true, y_pred) for i in range(y_pred.shape[-1])]

    def macro_recall(self, y_true, y_pred):
        class_count = y_pred.shape[-1]
        return K.sum([self.class_recall(i, y_true, y_pred) for i in range(class_count)])             / K.cast(class_count, K.floatx())

    def class_accuracy(self, class_label, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.cast(K.equal(y_true[:, class_label], y_pred[:, class_label]),
                    K.floatx())

    def all_class_accuracy(self, y_true, y_pred):
        return [np.mean(self.class_accuracy(i, y_true, y_pred)) for i in range(y_pred.shape[-1])]

    def average_accuracy(self, y_true, y_pred):
        class_count = y_pred.shape[-1]
        class_acc_list = [self.class_accuracy(i, y_true, y_pred) for i in range(class_count)]
        class_acc_matrix = K.concatenate(class_acc_list, axis=0)
        return K.mean(class_acc_matrix, axis=0)

    def class_f_measure(self, class_label, y_true, y_pred):
        precision = self.class_precision(class_label, y_true, y_pred)
        recall = self.class_recall(class_label, y_true, y_pred)
        return (2 * precision * recall) / (precision + recall + K.epsilon())

    def all_class_f_measure(self, y_true, y_pred):
        return [self.class_f_measure(i, y_true, y_pred) for i in range(y_pred.shape[-1])]

    def macro_f_measure(self, y_true, y_pred):
        precision = self.macro_precision(y_true, y_pred)
        recall = self.macro_recall(y_true, y_pred)
        return (2 * precision * recall) / (precision + recall + K.epsilon())


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 1/9

@log(logger)
@measures(ait_output, 'Accuracy', 'Precision', 'Recall', 'F−measure')
def calc_acc_all(y_test, y_pred) -> (float, float, float, float):
    calc = ACCCalculator()
    one_hot_y = to_categorical(y_test)

    return calc.average_accuracy(one_hot_y, y_pred).numpy() ,            calc.macro_precision(one_hot_y, y_pred).numpy() ,            calc.macro_recall(one_hot_y, y_pred).numpy() ,            calc.macro_f_measure(one_hot_y, y_pred).numpy()


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 2/9

@log(logger)
@measures(ait_output, 'AccuracyByClass', 'PrecisionByClass', 'RecallByClass', 'F−measureByClass', is_many=True)
def calc_acc_by_class( y_test, y_pred) -> (List[float], List[float], List[float], List[float]):
    calc = ACCCalculator()
    one_hot_y = to_categorical(y_test)

    return calc.all_class_accuracy(one_hot_y, y_pred) ,            [v.numpy() for v in calc.all_class_precision(one_hot_y, y_pred)] ,            [v.numpy() for v in calc.all_class_recall(one_hot_y, y_pred)] ,            [v.numpy() for v in calc.all_class_f_measure(one_hot_y, y_pred)]


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 3/9

@log(logger)
@downloads(ait_output, path_helper, 'ConfusionMatrixCSV', 'confusion_matrix.csv')
def save_confusion_matrix_csv(y_test, y_pred, file_path: str=None) -> None:

    cmx_data = confusion_matrix(y_test, K.argmax(y_pred))
    logger.info(cmx_data)
    np.savetxt(file_path, cmx_data, fmt='%d', delimiter=',')


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 4/9

@log(logger)
@resources(ait_output, path_helper, 'ConfusionMatrixHeatmap', 'confusion_matrix.png')
def save_confusion_matrix_heatmap(y_test, y_pred, file_path: str=None) -> None:

    y_pred = K.argmax(y_pred)

    labels = sorted(list(set(y_test)))
    cmx_data = confusion_matrix(y_test, y_pred, labels=labels)

    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    fig = plt.figure(dpi=100, figsize=(8,6))
    sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Predicted class')
    ax.set_ylabel('Actual class')
    ax.set_title('Plot of Confusion Matrix')

    # save as png
    plt.savefig(file_path)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 5/9

@log(logger)
@resources(ait_output, path_helper, 'ROC-curve', 'roc_curve.png')
def save_roc_curve(y_test, y_pred, n_classes: int, file_path: str=None) -> None:

    y_true = to_categorical(y_test)
    y_score = y_pred

    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    # Compute ROC curve and ROC area for each class
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_score[:, i], drop_intermediate=False)
        roc_auc[i] = auc(fpr[i], tpr[i])

    # First aggregate all false positive rates
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])

    # Finally average it and compute AUC
    mean_tpr /= n_classes

    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    # Plot all ROC curves
    plt.figure(dpi=100, figsize=(8,6))
    plt.plot(fpr["micro"], tpr["micro"],
            label='micro-average ROC curve (area = {0:0.2f})'
                ''.format(roc_auc["micro"]),
            color='deeppink', linestyle=':', linewidth=4)

    plt.plot(fpr["macro"], tpr["macro"],
            label='macro-average ROC curve (area = {0:0.2f})'
                ''.format(roc_auc["macro"]),
            color='navy', linestyle=':', linewidth=4)

    colors = cycle(['#1f77b4',
                    '#ff7f0e',
                    '#2ca02c',
                    '#d62728',
                    '#9467bd',
                    '#8c564b',
                    '#e377c2',
                    '#7f7f7f',
                    '#bcbd22',
                    '#17becf'])

    #colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                label='ROC curve of class {0} (area = {1:0.2f})'
                ''.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Some extension of Receiver operating characteristic to multi-class')
    plt.legend(loc="lower right")
    plt.savefig(file_path)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 6/9

@log(logger)
@measures(ait_output, 'AUC')
def calc_auc(y_test, y_pred, multi_class: str, average: str) -> float:
    y_true = to_categorical(y_test)
    y_score = y_pred

    return roc_auc_score(y_true, y_score,
                         multi_class=multi_class,
                         average=average)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 7/9

@log(logger)
@resources(ait_output, path_helper, 'NGPredictImages', 'ng_predict_actual_class_{}.png')
def save_ng_predicts(X_test, y_test, y_pred, n_classes: int, file_path: str=None) -> List[str]:

    out_files = []
    y_true = y_test
    y_pred = K.argmax(y_pred)

    # unmach_classes={label:[{predict: index}] }
    unmach_classes={}
    for actual_class_no in range(n_classes):
        unmach_classes[actual_class_no] = {}
        for predict_class_no in range(n_classes):
            unmach_classes[actual_class_no][predict_class_no] = []

    for i in range(y_pred.shape[-1]):
        if y_true[i] != y_pred[i].numpy():
            unmach_classes[y_true[i]][y_pred[i].numpy()].append(i)

    # visualization
    def draw_digit(data, row, col, n, index) -> None:
        ax = plt.subplot(row, col, n)
        ax.axis("off")
        ax.set_title(str(index))
        plt.imshow(data, cmap = "gray")

    def draw_text(text, row, col, n) -> None:
        ax = plt.subplot(row, col, n)
        ax.axis("off")

        # build a rectangle in axes coords
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        ax.text(0.5*(left+right), 0.5*(bottom+top), text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=12, color='black',
            transform=ax.transAxes)

    show_size = 10 + 1
    for actual_class_no in range(n_classes):
        fig = plt.figure(figsize=(n_classes,show_size))
        fig.suptitle('actual class.{}'.format(actual_class_no), fontsize=20)
        unmachies = unmach_classes[actual_class_no]
        for predict_class_no in range(n_classes):
            indexes = unmach_classes[actual_class_no][predict_class_no]
            offset = predict_class_no * show_size + 1
            draw_text('predict\nclass\n{}'.format(predict_class_no), n_classes, show_size, offset)

            image_count = 0
            for index in indexes:
                offset += 1
                draw_digit(X_test[index], n_classes, show_size, offset, index)
                # 11枚分以上は読み捨て
                image_count += 1
                if image_count >= 10:
                    break

        out_file = file_path.format(actual_class_no)
        out_files.append(out_file)
        plt.savefig(out_file)

    return out_files


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 8/9

@log(logger)
@downloads(ait_output, path_helper, 'PredictionResult', 'prediction.csv')
def save_prediction_result(y_test, y_pred, file_path: str=None) -> None:

    # Label + PredictProva
    out_data = np.hstack([y_test.reshape(y_test.shape[0], 1), y_pred])

    index = [str(i) for i in range(1, y_test.shape[0]+1)]
    columns = ['Label']+[f'PredictionProva_Class_{i}' for i in range(1,y_pred.shape[1]+1)]
    df = pd.DataFrame(data=out_data, index=index, columns=columns, dtype='float')

    df.to_csv(file_path)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################
# 9/9

@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> None:

    shutil.move(get_log_path(), file_path)


# In[ ]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:
    image_px_size = 28

    # インベントリのMNISTラベル・画像を読み込み
    mnist = MNIST()
    X_test = mnist.load_image(ait_input.get_inventory_path('test_set_images'), image_px_size)
    y_test = mnist.load_label(ait_input.get_inventory_path('test_set_labels'))

    # 前処理として、画像を最大値255で割って0.0 - 1.0に規格化
    X_test_normalize = X_test / 255

    # モデル読み込み
    model = tf.keras.models.load_model(ait_input.get_inventory_path('trained_model'))
    logger.info(get_summary_text(model))

    # 推論
    y_pred = model.predict(X_test_normalize)

    # 全体精度評価値(measure)
    calc_acc_all(y_test=y_test, y_pred=y_pred)

    # クラス別精度評価値(measure)
    calc_acc_by_class(y_test=y_test, y_pred=y_pred)

    # 混同行列(CSV)
    save_confusion_matrix_csv(y_test=y_test, y_pred=y_pred)

    # 混同行列(PNG)
    save_confusion_matrix_heatmap(y_test=y_test, y_pred=y_pred)

    # ROC曲線(PNG)
    save_roc_curve(y_test=y_test, y_pred=y_pred, 
                    n_classes=ait_input.get_method_param_value('class_count'))

    # AUC(measure)
    calc_auc(y_test=y_test, y_pred=y_pred,
              multi_class=ait_input.get_method_param_value('auc_multi_class'),
              average=ait_input.get_method_param_value('auc_average'))

    # NG画像(PNG)
    save_ng_predicts(X_test=X_test, y_test=y_test, y_pred=y_pred, 
                      n_classes= int(ait_input.get_method_param_value('class_count')))

    # PredictionResult(CSV)
    save_prediction_result(y_test=y_test, y_pred=y_pred)

    # log(Text)
    move_log()


# In[ ]:


#########################################
# area:entory point
# do not edit
#########################################
if __name__ == '__main__':
    main()


# In[ ]:


#########################################
# area:license attribute set
# should edit
#########################################
ait_owner='AIST'
ait_creation_year='2020'


# In[ ]:


#########################################
# area:prepare deproy
# do not edit
#########################################

if not is_ait_launch:
    from ait_sdk.deploy import prepare_deploy
    from ait_sdk.license.license_generator import LicenseGenerator
    
    current_dir = get_ipython().run_line_magic('pwd', '')
    prepare_deploy(ait_manifest, ait_sdk_name, current_dir, requirements_path, is_remote_deploy=True)
    
    # output License.txt
    license_generator = LicenseGenerator()
    license_generator.write('../top_dir/LICENSE.txt', ait_creation_year, ait_owner)


# In[ ]:




