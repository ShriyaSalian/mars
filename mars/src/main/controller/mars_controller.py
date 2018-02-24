from flask import Flask, request
import mars_processor


app = Flask(__name__)


@app.route('/templates/model/create/', methods=['POST', 'GET'])
def model_template_create():
    if request.method == 'POST':
        result = mars_processor.create_model_template(request.form.get('template'))
        return result
    else:
        result = mars_processor.create_model_template(request.args.get('template'))
        return result


@app.route('/templates/model/get/', methods=['POST', 'GET'])
def model_template_get():
    if request.method == 'POST':
        result = mars_processor.get_model_template(request.form.get('template_id'))
        return result
    else:
        result = mars_processor.get_model_template(request.args.get('template_id'))
        return result


@app.route('/templates/attribute/create/', methods=['POST', 'GET'])
def attribute_template_create():
    if request.method == 'POST':
        return 'Using post method to create new attribute template'
    else:
        return 'Using get method to create new attribute template'


@app.route('/instances/model/add_one/', methods=['POST', 'GET'])
def model_instance_add_one():
    if request.method == 'POST':
        return 'Using post method to create one new model'
    else:
        return 'Using get method to create one new model'


@app.route('/instances/model/create_multiple/', methods=['POST', 'GET'])
def model_instance_add_multiple():
    if request.method == 'POST':
        return 'Using post method to multiple new models (bulk insert)'
    else:
        return 'Using get method to create multiple new models (bulk insert)'


@app.route('/instances/attribute/create_one/', methods=['POST', 'GET'])
def attribute_instance_create_one():
    if request.method == 'POST':
        return 'Using post method to create one new attribute'
    else:
        return 'Using get method to create one new attribute'


@app.route('/instances/attribute/create_multiple/', methods=['POST', 'GET'])
def attribute_instance_create_multiple():
    if request.method == 'POST':
        return 'Using post method to create multiple new attributes (bulk insert)'
    else:
        return 'Using get method to create multiple new attributes (bulk insert)'


if __name__ == '__main__':
    app.run(debug=True)
