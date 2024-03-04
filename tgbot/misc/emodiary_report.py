from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader


def generatePDFReport(title, emotions, path):

    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template('Report_template.html')

    data = {
        'title': title,
        'emotions': emotions
    }
    rendered_html = template.render(data)

    return HTML(string=rendered_html, base_url='base_url').write_pdf()

if __name__ == "__main__":
    title = "Emotional Diary Report"
    emotions = [
        {
            'entry_date': '2024-03-03',
            'emotion': 'Happy',
            'thoughts': 'Spent time with family',
            'activity': '8'
        },
        # Add more entries as needed
    ]
    path = '../../report_template'
    generatePDFReport(title, emotions, path)  