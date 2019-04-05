from etl_manager.etl import GlueJob
import os
import sys
import zipfile
import argparse

def main(job_role):
    package_name = 'gluejobutils'
    to_path = f'test/glue_test/glue_py_resources/{package_name}.zip'
    zf = zipfile.ZipFile(to_path, "w")
    zf.write(os.path.join(package_name, '__init__.py'))
    zf.write(os.path.join(package_name, 'datatypes.py'))
    zf.write(os.path.join(package_name, 's3.py'))
    zf.write(os.path.join(package_name, 'utils.py'))
    zf.write(os.path.join(package_name, 'dea_record_datetimes.py'))
    zf.write(os.path.join(package_name, 'df_transforms.py'))
    zf.write(os.path.join(package_name, 'data/data_type_conversion.json'))
    zf.close()

    g = GlueJob('test/glue_test/', bucket='alpha-gluejobutils', job_role=job_role)
    g.job_name = 'gluejobutils_unit_test'
    g.run_job()

    g.wait_for_completion(True)
    if g.job_run_state == 'SUCCEEDED':
        print("cleaning up job...")
        g.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_role")
    args = parser.parse_args()
    main(args.job_role)
