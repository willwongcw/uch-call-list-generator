from flask import Flask, render_template, request, send_file
import io
import pandas as pd
from openpyxl import load_workbook
from waitress import serve

from create_template import create_timetable
from generate_callList import runFile, format_output_excel

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/create_template", methods=["GET", "POST"])
def create_template():
    if request.method == "POST":
        year = request.form["year"]
        month = request.form["month"]
        doctor_names = request.form["doctor_names"].split("\n")

        # Call create_timetable function
        wb = create_timetable(year, month, doctor_names)

        # Write Excel to in-memory buffer
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        # Send file back to user
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="timetable.xlsx",
        )

    return render_template("create_template.html")


@app.route("/generate_call_list", methods=["GET", "POST"])
def generate_call_list():
    if request.method == "POST":
        f = request.files["file"]

        if f:
            # # Save file to temp path
            # temp_path = os.path.join(current_app.root_path, 'uploads')  
            # f.save(os.path.join(temp_path, f.filename))
            
            # Process the file (assuming runFile() is defined elsewhere)
            processed_data = runFile(f)

            # Delete the temporary file
            # os.remove(temp_path)
            
            output = io.BytesIO()

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                # Assuming processed_data is a tuple containing all necessary values
                df_with_headers = processed_data[0]
                expected_metrics = processed_data[1]
                # year = processed_data[2]
                # month = processed_data[3]
                # total_calls = processed_data[4]
                # total_sat_calls = processed_data[5]
                # total_sun_calls = processed_data[6]
                # three_day_calls = processed_data[7]
                # four_days_calls = processed_data[8]
                # five_day_calls = processed_data[9]
                # six_day_calls = processed_data[10]
                # seven_day_calls = processed_data[11]

                # Write the dataframes to the Excel writer
                df_with_headers.to_excel(writer, index=False, startrow=2, startcol=5)
                expected_metrics.to_excel(writer, sheet_name="Sheet1", startrow=3, header=True, index=False)

                # Format the output (assuming format_output_excel() is defined elsewhere)
                format_output_excel(writer, *processed_data[2:])

            # Rewind the buffer
            output.seek(0)

            # Send the file to the client
            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name="call_list.xlsx",
            )

    return render_template("generate_call_list.html")




if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
