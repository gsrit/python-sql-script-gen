from flask import Flask, render_template, request
from datetime import datetime
import pytz

app = Flask(__name__)

# Render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get the selected date and time and timezone from the form
    selected_date_time = request.form['datetime']
    selected_time_zone = request.form['timezone']

    # Convert the selected date and time to UTC
    local_tz = pytz.timezone(selected_time_zone)
    utc_dt = local_tz.localize(datetime.strptime(selected_date_time, '%Y-%m-%dT%H:%M')).astimezone(pytz.utc)
    
    # Convert UTC datetime to the desired timezones
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_dt = utc_dt.astimezone(ist_tz)

    est_tz = pytz.timezone('US/Eastern')
    est_dt = utc_dt.astimezone(est_tz)

    cdt_tz = pytz.timezone('US/Central')
    cdt_dt = utc_dt.astimezone(cdt_tz)

    mst_tz = pytz.timezone('US/Mountain')
    mst_dt = utc_dt.astimezone(mst_tz)

    pdt_tz = pytz.timezone('US/Pacific')
    pdt_dt = utc_dt.astimezone(pdt_tz)

    canadian_tz = pytz.timezone('Canada/Eastern')  # Example: Eastern Canadian Time
    canadian_dt = utc_dt.astimezone(canadian_tz)

    # Generate SQL script
    sql_script = f"""-- Clean out Reporting Tables
    DELETE FROM [Trans].[ReportingCallFlows] WHERE TransactionDateTime < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    DELETE FROM [Trans].[ReportingEvents] WHERE TransactionDateTime < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    DELETE FROM [Trans].[ReportingTimers] WHERE TransactionDateTime < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    DELETE FROM [Trans].[ReportingTransfers] WHERE TransactionDateTime < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    -- Clean out Smart Track Tables
    DELETE FROM [Trans].[TrackAuthentications] WHERE DatePosted < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    DELETE FROM [Trans].[TrackManualAuthenticationHistory] WHERE [DateTime] < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    DELETE FROM [Trans].[TrackViolations] WHERE DatePosted < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'
    -- Other Tables
    DELETE FROM [Trans].[CallPlatformSmartAppsIds] WHERE PostedDate < '{utc_dt.strftime('%Y-%m-%d %H:%M')}'"""

    return render_template('result.html', sql_script=sql_script, 
                           selected_datetime=selected_date_time, 
                           selected_timezone=selected_time_zone,
                           ist_datetime=ist_dt.strftime('%Y-%m-%d %H:%M IST'), 
                           canada_datetime=canadian_dt.strftime('%Y-%m-%d %H:%M Canadian Time'))

if __name__ == '__main__':
    app.run(debug=True)
