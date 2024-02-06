# UCH Radiology Call List Generator - GitHub README

## How to Use the Program

### Web Version Access:
1. Navigate to the online tool at [UCH On-Call List Generator](https://willwongcw.pythonanywhere.com/).
   - Please note that this is hosted on Pythonanywhere's free web platform, and you might need to refresh the page if you encounter an error upon visiting.

### Template Creation:
2. Click on **"First Step: Create Template"**.
   1. Input the desired year (e.g., `2024`) and month (e.g., `6`).
   2. Enter the list of doctors, each on a new line.
   3. Click `Submit` to proceed.
   4. Download the generated Excel template.

### Template Editing:
3. Open the downloaded Excel template and make your modifications:
   1. Mark days a doctor shouldn't be on call with an `"x"` in the corresponding cells.
   2. Indicate days a doctor should be on call with a `"1"` in the necessary cells.
   3. In the first column labeled `"expected_total"`, enter the expected number of calls for each doctor (use integers only). This doesn't need to be exact.
      - For example, with 7 doctors and 30 days in a month, inputting `4` for every doctor is reasonable. Adjust the numbers lower or higher for fewer or more calls.
   4. **IMPORTANT**: Do not alter any other cells in the template. If you need to change the number of doctors or the template month, create a new template using the **First Step**.

### Call List Generation:
4. Proceed to **"Second Step: Generate Call List"**.
   1. Click `Choose File` and upload the edited Excel file.
   2. Click `Submit` and wait briefly. Then, download the generated call list.

### Understanding the Generated Call List:
- In the Excel file:
  - `"F"` marks enforced call requests.
  - `"1"` represents calls assigned by the program.
  - `"x"` indicates dates you opted to avoid for calls.

### Tips for Fair Weekend Calls:
- To balance weekend call duties, consider assigning `"1"` for each weekend date in the Excel template for individual doctors before uploading the file in Step 2.
- Experiment with different weekend call configurations to evaluate and select the best-generated call list.

Remember that the key to success with the UCH On-Call List Generator is precision in the initial template setup and considerate planning of enforced and avoided on-call days. Good luck!
