# Build a webpage to upload images and show visual similarity of two images
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from product import product, ResNet50Feature
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Upload Image</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <h1>Upload another Image</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
# A list to save image names for immediate computation use.
imglist = []
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            imglist.append(filename)
            # Show the most recent upload image names. At most two names in the list. This is printing in terminal.
            print(imglist)
            # When there are two images in the list, we compute the similarity of these two images.
            if len(imglist) == 2:
                    p1 = product()
                    p2 = product()
                    p1.readImage('./images/'+imglist[0])
                    p2.readImage('./images/'+imglist[1])
                    p1.feature()
                    p2.feature()
                    result_e = p1.similarity(p2,'Euclidean')
                    result_c = p1.similarity(p2,'Cosine')
                    result_p = p1.similarity(p2,'Pearson')
                    # Clear the list for next time use. Thus, the previous images uploaded won't affect next time computation and save compute memory.
                    imglist.clear()
                    result_e_show = '<div style="color: black; size: 14px;"> The Euclidean distance of two images is: <p style="color:red"> {} </p ></div>'.format(result_e)
                    result_c_show = '<div style="color: black; size: 14px;"> The Cosine similarity of two images is: <p style="color:red"> {} </p ></div>'.format(result_c)
                    result_p_show = '<div style="color: black; size: 14px;"> The Pearson coefficient of two images is: <p style="color:red"> {} </p ></div>'.format(result_p)
                    return html+'</br>'+result_e_show+'</br>'+result_c_show+'</br>'+result_p_show
            return html + '<br><img src=' + file_url + '>'
    return html

if __name__ == '__main__':
    app.run()