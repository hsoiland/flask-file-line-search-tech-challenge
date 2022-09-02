from flask import Flask, request, jsonify
import re
from service import FileSearchService
import logging
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def get_file_rows():
    params = request.json
    filename, todate, fromdate = params["filename"], params["to"], params["from"]
    logging.info(f'APP - get_file_rows: Starting - filename: %s from: %s to: %s' %(filename, todate, fromdate))

    try:
        service = FileSearchService(f'/app/test-files/%s' %filename, fromdate, todate)
        listOfLines = service.get_file_rows_by_date_range()
        logging.info("APP - get_file_rows: Success")
        return jsonify(listOfLines)
    except:
        logging.error("APP - get_file_rows: Failed")
        return jsonify([])
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8279)
    