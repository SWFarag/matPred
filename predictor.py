from werkzeug.utils import secure_filename
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import zipfile

class MatPredidctor:

    def __init__(self):
        pass

    # For a given file, return whether it's an allowed type or not
    def allowed_file(self, filename, app):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


    def uploadFiles(self, uploaded_files, app):
        # Get the name of the uploaded files
        filenames_dic = {}
        bad_filenames_dic = {}
        for file in uploaded_files:
            print file
            if file:
               # Check if the file is one of the allowed types/extensions
               if self.allowed_file(file.filename, app):
                   # Make the filename safe, remove unsupported chars
                   filename = secure_filename(file.filename)
                   if filename.endswith(".zip"):
                       self.unzipFile(file, app,filename)
                       onlyfiles = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
                       for f in onlyfiles:
                           x_file=f = open(app.config['UPLOAD_FOLDER']+f,'w')
                           filenames_dic[filename]=x_file
                   else:
                       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                       # Save the filename into a list, we'll use it later
                       filenames_dic[filename]=file
                       # Redirect the user to the uploaded_file route, which
                       # will basicaly show on the browser the uploaded file
                       # Load an html page with a link to each uploaded file
               else:
                   filename = secure_filename(file.filename)
                   bad_filenames_dic[filename] = "wrong-extension"
            else:filenames_dic
        print "el-Hoba", filenames_dic
        return filenames_dic, bad_filenames_dic

    def modelPrediction(self, path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        dic_files={}
        for i in range (len(onlyfiles)):
            dic_files[i]=[f,f,f,f]
        extracted_data=pd.DataFrame.from_dict(dic_files, orient='index', dtype=None)
        results=extracted_data.rename(columns={0:"name",1:"value",2:"name",3    :"value"})
        self.deleteUploadedFiles(path)
        return results

    def deleteUploadedFiles(self, path):
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def tohtml_library_parser(self, df, tableId):
    		cols = df.columns
    		s = '''<table id="''' + tableId + '''" class="display table table-striped table-bordered" width="100%">'''
    		s = s + '''
    	        <thead>
    	            <tr>'''
    		for col in cols:
    			temp = '''
    	                <th>''' + str(col) + '''</th>
    	            '''
    			s = s + temp
    		end_header = '''</tr>
    	        </thead>'''
    		s = s + end_header

    		s = s + '''
    	        <tfoot>
    	            <tr>'''
    		for col in cols:
    			temp = '''
    				<th>''' + str(col) + '''</th>
    				'''
    			s = s + temp

    		end_foot = '''</tr>
    	        </tfoot>'''
    		s = s + end_foot

    		s = s + '''
    	        <tbody>'''
    		for index, row in df.iterrows():
    			s = s + '''
    	            <tr>'''
    			for i in xrange(0, len(row)):
    				line = str(row[i])
    				if len(line) <= 50:
    					temp = '''
    	                    <td>''' + line + '''</td>
    	                    '''
    					s = s + temp
    				else:
    					temp = '''
    	                    <td>''' + line[0:50] + '''...''' + '''</td>
    	                    '''
    					s = s + temp
    			s = s + '''
    	            </tr>'''
    		end_table = '''
    	        </tbody>
    	    </table>'''
    		s = s + end_table
    		s = s.encode('ascii', 'xmlcharrefreplace')
    		return s

    def unzipFile(self, file,app,filename):
        zip_ref = zipfile.ZipFile(file, 'r')
        print zip_ref.namelist()
        zip_ref.extractall(app.config['UPLOAD_FOLDER'])
        zip_ref.close()
