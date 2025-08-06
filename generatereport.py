import csv
from fpdf import FPDF
from collections import defaultdict


def read_and_analyze_data(filename):
    department_data = defaultdict(list)
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                dept = row['Department']
                salary = float(row['Salary'])
                department_data[dept].append(salary)
            except (KeyError, ValueError):
                pass 
    return department_data

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Employee Salary Analysis Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def report_body(self, department_data):
        self.set_font('Arial', '', 12)
        for dept, salaries in department_data.items():
            avg_salary = sum(salaries) / len(salaries)
            total_salary = sum(salaries)

          
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, f'Department: {dept}', ln=True)

            self.set_font('Arial', '', 12)
            self.cell(0, 10, f'  Total Employees: {len(salaries)}', ln=True)
            self.cell(0, 10, f'  Total Salary: ${total_salary:,.2f}', ln=True)
            self.cell(0, 10, f'  Average Salary: ${avg_salary:,.2f}', ln=True)
            self.ln(5)

def main():
    data = read_and_analyze_data('data.csv')
    if not data:
        print("No data found. Please check data.csv.")
        return
    pdf = PDFReport()
    pdf.add_page()
    pdf.report_body(data)
    pdf.output('salary_report.pdf')
    print("✅ PDF report 'salary_report.pdf' generated successfully.")

if __name__ == "__main__":
    main()
