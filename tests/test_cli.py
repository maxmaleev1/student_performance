import os
import sys
import csv
import subprocess


def write_csv(path, rows):
    '''Создаёт CSV-файл с заголовками и переданными строками данных'''
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['student_name', 'subject',
                   'teacher_name', 'date', 'grade'])
        w.writerows(rows)


def run_cli(args, cwd):
    '''Запускает CLI-скрипт с аргументами и возвращает (код, stdout, stderr)'''
    proc = subprocess.run(
        [sys.executable, 'main.py'] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    out = proc.stdout or ''
    err = proc.stderr or ''
    return proc.returncode, out, err


def test_student_performance_two_files(tmp_path):
    '''
    Проверяет отчёт по двум CSV на:
    - корректность среднего балла студентов
    - сортировку по убыванию среднего балла
    '''
    f1 = tmp_path / 'a.csv'
    f2 = tmp_path / 'b.csv'
    write_csv(f1, [
        ['Иванов Иван', 'Математика', 'Петров', '2024-01-01', '5'],
        ['Сидоров Павел', 'Математика', 'Петров', '2024-01-01', '4'],
    ])
    write_csv(f2, [
        ['Иванов Иван', 'Физика', 'Иванова', '2024-01-02', '3'],
        ['Сидоров Павел', 'Физика', 'Иванова', '2024-01-02', '5'],
        ['Кузнецова Анна', 'Физика', 'Иванова', '2024-01-02', '5'],
    ])
    code, out, err = run_cli(
        ['--files', str(f1), str(f2), '--report', 'student-performance'],
        cwd=os.getcwd(),
    )
    assert code == 0, err

    lines = out.splitlines()
    ivanov_line = next(Line for Line in lines if 'Иванов Иван' in Line)
    sidorov_line = next(Line for Line in lines if 'Сидоров Павел' in Line)
    kuz_line = next(Line for Line in lines if 'Кузнецова Анна' in Line)

    assert '4' in ivanov_line
    assert '4.5' in sidorov_line or '4.50' in sidorov_line
    assert '5' in kuz_line

    kuz_idx = lines.index(kuz_line)
    sidorov_idx = lines.index(sidorov_line)
    ivanov_idx = lines.index(ivanov_line)
    assert kuz_idx < sidorov_idx < ivanov_idx


def test_student_performance_single_file(tmp_path):
    '''
    Проверяет отчёт по одному CSV:
    - усреднение оценок одного студента
    - корректную сортировку по убыванию
    '''
    f1 = tmp_path / 'only.csv'
    write_csv(f1, [
        ['Петрова Мария', 'Математика', 'Петров', '2024-01-01', '2'],
        ['Смирнов Алексей', 'Математика', 'Петров', '2024-01-01', '5'],
        ['Петрова Мария', 'Физика', 'Иванова', '2024-01-02', '4'],
    ])
    code, out, err = run_cli(
        ['--files', str(f1), '--report', 'student-performance'],
        cwd=os.getcwd(),
    )
    assert code == 0, err

    lines = out.splitlines()
    petrova_line = next(Line for Line in lines if 'Петрова Мария' in Line)
    smirnov_line = next(Line for Line in lines if 'Смирнов Алексей' in Line)

    assert any(x in petrova_line for x in ('3', '3.0', '3.00'))

    smirnov_idx = lines.index(smirnov_line)
    petrova_idx = lines.index(petrova_line)
    assert smirnov_idx < petrova_idx
