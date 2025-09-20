import argparse
from .registry import available_reports


def build_parser():
    '''Создаёт парсер аргументов командной строки для выбора файлов и отчёта'''
    parser = argparse.ArgumentParser(
        description='Student performance reports'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Paths to CSV files'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=available_reports(),
        help='Report name (e.g. student-performance)'
    )
    return parser
