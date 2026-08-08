#!/usr/bin/env python3
"""
Генерация финального отчёта о тестировании PRTV.pro
Автоматически создаёт Word-документ с метриками, багами и рекомендациями
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import openpyxl
from datetime import datetime

def load_test_cases(filepath):
    """Загрузка тест-кейсов из Excel"""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    
    test_cases = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:  # Если есть ID
            test_cases.append({
                'id': row[0],
                'type': row[1],
                'module': row[2],
                'name': row[3],
                'status': row[9],
                'bug_id': row[10] if len(row) > 10 else None
            })
    
    return test_cases

def load_bug_reports(filepath):
    """Загрузка баг-репортов из Excel"""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    
    bugs = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:  # Если есть ID
            bugs.append({
                'id': row[0],
                'name': row[1],
                'severity': row[2],
                'priority': row[3],
                'preconditions': row[4],
                'steps': row[5],
                'expected': row[6],
                'actual': row[7],
                'attachments': row[8],
                'tc': row[9] if len(row) > 9 else None
            })
    
    return bugs

def calculate_metrics(test_cases, bugs):
    """Расчёт метрик"""
    total = len(test_cases)
    passed = sum(1 for tc in test_cases if tc['status'] == 'Passed')
    failed = sum(1 for tc in test_cases if tc['status'] == 'Failed')
    blocked = sum(1 for tc in test_cases if tc['status'] == 'Blocked')
    not_tested = sum(1 for tc in test_cases if tc['status'] == 'Not Tested')
    
    high_bugs = sum(1 for bug in bugs if bug['severity'] == 'High')
    medium_bugs = sum(1 for bug in bugs if bug['severity'] == 'Medium')
    low_bugs = sum(1 for bug in bugs if bug['severity'] == 'Low')
    
    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'blocked': blocked,
        'not_tested': not_tested,
        'pass_rate': (passed / total * 100) if total > 0 else 0,
        'total_bugs': len(bugs),
        'high_bugs': high_bugs,
        'medium_bugs': medium_bugs,
        'low_bugs': low_bugs
    }

def create_report(test_cases, bugs, metrics, output_file):
    """Создание Word-отчёта"""
    doc = Document()
    
    # Заголовок
    title = doc.add_heading('Отчёт о тестировании PRTV.pro', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Метаинформация
    meta = doc.add_paragraph()
    meta.add_run('Дата: ').bold = True
    meta.add_run(f'{datetime.now().strftime("%d %B %Y")}\n')
    meta.add_run('Тестировщик: ').bold = True
    meta.add_run('Всеволод\n')
    meta.add_run('Версия приложения: ').bold = True
    meta.add_run('v2.0.102\n')
    
    doc.add_paragraph()
    
    # Executive Summary
    doc.add_heading('1. Executive Summary', 1)
    doc.add_paragraph(
        f'Проведено функциональное тестирование PRTV.pro по {metrics["total"]} тест-кейсам. '
        f'Охвачено 18 модулей системы.'
    )
    
    doc.add_paragraph('Ключевые результаты:', style='List Bullet')
    doc.add_paragraph(f'✅ {metrics["pass_rate"]:.1f}% тест-кейсов пройдено ({metrics["passed"]}/{metrics["total"]})', style='List Bullet 2')
    doc.add_paragraph(f'⚠️ {metrics["total_bugs"]} багов найдено ({metrics["high_bugs"]} критических)', style='List Bullet 2')
    doc.add_paragraph(f'🔴 {metrics["blocked"]} тест-кейсов заблокированы', style='List Bullet 2')
    
    doc.add_page_break()
    
    # Метрики
    doc.add_heading('2. Метрики', 1)
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Метрика'
    hdr_cells[1].text = 'Значение'
    
    metrics_data = [
        ('Всего тест-кейсов', str(metrics['total'])),
        ('Passed', f'{metrics["passed"]} ({metrics["pass_rate"]:.1f}%)'),
        ('Failed', f'{metrics["failed"]} ({metrics["failed"]/metrics["total"]*100:.1f}%)'),
        ('Blocked', f'{metrics["blocked"]} ({metrics["blocked"]/metrics["total"]*100:.1f}%)'),
        ('Not Tested', f'{metrics["not_tested"]} ({metrics["not_tested"]/metrics["total"]*100:.1f}%)'),
        ('Всего багов', str(metrics['total_bugs'])),
        ('High', str(metrics['high_bugs'])),
        ('Medium', str(metrics['medium_bugs'])),
        ('Low', str(metrics['low_bugs'])),
    ]
    
    for metric, value in metrics_data:
        row_cells = table.add_row().cells
        row_cells[0].text = metric
        row_cells[1].text = value
    
    doc.add_page_break()
    
    # Критические баги
    doc.add_heading('3. Критические баги (High Severity)', 1)
    
    high_bugs = [bug for bug in bugs if bug['severity'] == 'High']
    
    for bug in high_bugs[:10]:  # Топ-10 критических
        doc.add_heading(f'🔴 {bug["id"]}: {bug["name"]}', 2)
        p = doc.add_paragraph()
        p.add_run('TC: ').bold = True
        p.add_run(f'{bug["tc"]}\n')
        p.add_run('Факт: ').bold = True
        p.add_run(f'{bug["actual"]}\n')
    
    doc.add_page_break()
    
    # Рекомендации
    doc.add_heading('4. Рекомендации', 1)
    
    doc.add_paragraph('Продукт НЕ готов к продакшену из-за:', style='List Bullet')
    doc.add_paragraph('🔴 Неработающих интеграций (рестораны, соцсети, RSS)', style='List Bullet 2')
    doc.add_paragraph('🔴 Неработающего ТВ-приложения', style='List Bullet 2')
    doc.add_paragraph('🔴 Критических проблем мобильной версии', style='List Bullet 2')
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Рекомендация: ').bold = True
    p.add_run('исправить 18 High-багов перед релизом.')
    
    # Сохранение
    doc.save(output_file)
    print(f'✅ Отчёт сохранён: {output_file}')

def main():
    # Пути к файлам
    test_cases_file = '../TEST-CASES/TestCases_final.xlsx'
    bug_reports_file = '../BUG-REPORTS/BugReports_PROD_final.xlsx'
    output_file = '../REPORTS/detailed_report.docx'
    
    # Загрузка данных
    print('Загрузка тест-кейсов...')
    test_cases = load_test_cases(test_cases_file)
    print(f'  Загружено {len(test_cases)} тест-кейсов')
    
    print('Загрузка баг-репортов...')
    bugs = load_bug_reports(bug_reports_file)
    print(f'  Загружено {len(bugs)} баг-репортов')
    
    # Расчёт метрик
    print('Расчёт метрик...')
    metrics = calculate_metrics(test_cases, bugs)
    print(f'  Pass Rate: {metrics["pass_rate"]:.1f}%')
    print(f'  Всего багов: {metrics["total_bugs"]}')
    
    # Создание отчёта
    print('Создание отчёта...')
    create_report(test_cases, bugs, metrics, output_file)
    
    print('✅ Готово!')

if __name__ == '__main__':
    main()
