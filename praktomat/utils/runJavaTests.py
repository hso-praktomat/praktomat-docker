import os
import subprocess
import sys
import yaml


class Config:
    def __init__(self, test_dir, assignments):
        self.test_dir = test_dir
        self.assignments = assignments


class Assignment:
    def __init__(self, num, test_filter):
        self.num = num
        self.test_filter = test_filter


def read_config(solution_dir):
    content = ''
    with open(os.path.join(solution_dir, 'check.yml'), 'r', encoding='utf-8') as file:
        content = file.read()
    ymlDict = yaml.load(content, yaml.FullLoader)
    test_dir = os.path.join(solution_dir, ymlDict['test-dir'])
    assignments = []
    for k, v in ymlDict['assignments'].items():
        assignments.append(Assignment(k, v['test-filter']))
    return Config(test_dir, assignments)


def exec_gradle(build_file, task, test_dir, test_filter, student_dir):
    completed_process = subprocess.run(
        [
            'gradle',
            '-b',
            build_file,
            '-PtestFilter=' + test_filter,
            '-PtestDir=' + test_dir,
            '-PstudentDir=' + student_dir,
            task,
            '--rerun-tasks',
        ]
    )
    return completed_process.returncode


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Not enough arguments')
        sys.exit(1)

    mode = sys.argv[1]
    student_dir = sys.argv[2]
    solution_dir = sys.argv[3]

    build_file = os.path.join(solution_dir, 'build.gradle')
    config = read_config(solution_dir)

    exit_code = 0
    if mode == 'compile':
        exit_code = exec_gradle(
            build_file=build_file,
            task='compileJava',
            test_dir='NOT_EXISTING_TEST_DIR',
            test_filter='*',
            student_dir=student_dir,
        )
    elif mode == 'runUserTests':
        exit_code = exec_gradle(
            build_file=build_file,
            task='test',
            test_dir=student_dir,
            test_filter='*',
            student_dir=student_dir,
        )
    elif mode == 'runSolutionTests':
        for assignment in config.assignments:
            print()
            tmp_exit_code = exec_gradle(
                build_file=build_file,
                task='test',
                test_dir=config.test_dir,
                test_filter=assignment.test_filter,
                student_dir=student_dir,
            )
            print()

            if tmp_exit_code != 0:
                exit_code = tmp_exit_code
    else:
        print('Unsupported mode: ' + mode)
        exit_code = 1

    sys.exit(exit_code)
