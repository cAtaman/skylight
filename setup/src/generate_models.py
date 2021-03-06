import os
from imports import model_template_path, models_dir

start_session = 2003
curr_session = 2019

sessions = range(start_session, curr_session + 1)
for session in sessions:
    model = open(os.path.join(models_dir, '_{0}_{1}.py'.format(session, session + 1)), 'w')
    model_template = open(model_template_path)
    lines = model_template.readlines()
    for index in range(len(lines)):
        lines[index] = lines[index].replace(
            '##NAME##', '{0}-{1}'.format(session, session + 1)).replace(
            '##NAME_2##', '_{0}_{1}'.format(session, session + 1))
    model.writelines(lines)
    model.close()

print('Done')
