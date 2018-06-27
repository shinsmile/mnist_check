# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist
from neural_net.two_layer_net import TwoLayerNet

#Flask関係のimport
from flask import Flask, render_template
from flask import request, jsonify
import json

app = Flask(__name__)


@app.route('/')
def index():
   return render_template('check.html')

@app.route('/postText', methods=['POST'])
def learn_and_judge():
    text = request.json['x']
    data = list(text.values())

    # データの読み込み
    (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

    network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

    iters_num = 10000  # 繰り返しの回数を適宜設定する
    train_size = x_train.shape[0]
    batch_size = 100
    learning_rate = 0.1

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    iter_per_epoch = max(train_size / batch_size, 1)

    for i in range(iters_num):
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        # 勾配の計算
        #grad = network.numerical_gradient(x_batch, t_batch)
        grad = network.gradient(x_batch, t_batch)

        # パラメータの更新
        for key in ('W1', 'b1', 'W2', 'b2'):
            network.params[key] -= learning_rate * grad[key]

        loss = network.loss(x_batch, t_batch)
        train_loss_list.append(loss)

        if i % iter_per_epoch == 0:
            train_acc = network.accuracy(x_train, t_train)
            test_acc = network.accuracy(x_test, t_test)
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

    y = TwoLayerNet.predict(network, data)
    x = np.argmax(y)
    print(x)
    result = str(x)

    return_data = {"result":result}
    return jsonify(ResultSet=json.dumps(return_data))


if __name__ == '__main__':
   app.run(host="127.0.0.1", port=8080)
