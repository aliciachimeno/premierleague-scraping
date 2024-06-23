import os

def create_directories():
    if not os.path.exists('files'):
        os.makedirs('files/stats')
        os.makedirs('files/results')