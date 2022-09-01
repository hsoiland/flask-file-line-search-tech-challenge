from flask import Flask, request, jsonify
import re
from service import FileSearchService
app = Flask(__name__)
app.debug = True

ISO_8601_RGX = "^\d{4}-(0\d|1[0-2])-([0-2]\d|3[0-2])(T(([01]\d|2[0-4]):([0-5]\d)(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])([\.,]\d+)?))?([+-]\d\d(:[0-5]\d)?|Z)?$"

@app.route('/', methods=['GET', 'POST'])
def get_file_rows():
    params = request.json
    if not valid_date(params["to"]) and not valid_date(params["from"]):
        return jsonify([])
    service = FileSearchService(params["filename"], params["to"], params["from"])
    listOfLines = service.get_file_rows_by_date_range()
    return jsonify(listOfLines)

def valid_date(date: str)-> bool:
    return re.search(ISO_8601_RGX, date) is not None


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8279)
    