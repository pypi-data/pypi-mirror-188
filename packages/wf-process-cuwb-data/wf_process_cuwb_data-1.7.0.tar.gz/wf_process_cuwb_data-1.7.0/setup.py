# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['process_cuwb_data',
 'process_cuwb_data.filters',
 'process_cuwb_data.honeycomb_service',
 'process_cuwb_data.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17,<2.0',
 'click-log>=0.4.0,<0.5.0',
 'click>=8.0.0,<9.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'nocasedict>=1.0.2,<2.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-slugify>=8.0.0,<9.0.0',
 'pyyaml>=6.0,<7.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'wf-geom-render>=0.3.0,<0.4.0',
 'wf-honeycomb-io>=2.0.0,<3.0.0',
 'wf-process-pose-data>=6.2.0,<7.0.0']

entry_points = \
{'console_scripts': ['process_cuwb_data = process_cuwb_data.cli:cli']}

setup_kwargs = {
    'name': 'wf-process-cuwb-data',
    'version': '1.7.0',
    'description': 'Tools for reading, processing, and writing CUWB data',
    'long_description': '# process_cuwb_data\n\nTools for reading, processing, and writing CUWB data\n\n## Setup\n\nThis project uses Poetry. Please make sure Poetry is installed before continuing.\n\n1. Copy `.env.template` to `.env` and update variables\n\n\n2. Install packages\n\n    `just install`\n\n    You may need to install pybind11 `brew install pybind11`\n    And you may need to manually install cython and numpy `pip install numpy cython pythran`\n\n## Tasks\n\n### Export pickled UWB data\n\nWorking with Honeycomb\'s UWB endpoint can be painfully slow. For that reason there is an option to export pickled UWB data and provide that to subsequent inference commands.\n\n     process_cuwb_data \\\n        fetch-cuwb-data \\\n        --environment greenbrier \\\n        --start 2021-04-20T9:00:00-0500 \\\n        --end 2021-04-20T9:05:00-0500 \\\n        --annonymize\n\n\n### Export pickled Motion Feature data\n\nThe tray carry model doesn\'t read raw UWB data. It reads a version of UWB data that has been prepared for inference. This feature data can be generated and fed into subsequent commands.\n\n     process_cuwb_data \\\n        fetch-motion-features \\\n        --environment greenbrier \\\n        --start 2021-05-27T14:13:00 \\\n        --end 2021-05-27T14:15:00 \\\n        --cuwb-data ./output/uwb_data/uwb-greenbrier-20210527-141300-20210527-141500.pkl \\\n        --annonymize\n\n\n### Generate Tray Centroids\n\nTray centroids, or tray positions, are the most likely locations of a tray\'s shelf or at-rest position. Tray locations are used, for example, to determine when someone is picking a tray up off the shelf as opposed to picking up a tray from a workstation. Note that tray locations are computed based on the window of time provided to the function. If the function ran on 10 minutes of classroom data, it\'d likely produce a different idea of tray\'s shelf locations than if the function was run on 9 hours of classroom activity.  \n\n    process_cuwb_data \\\n        estimate-tray-centroids \\\n        --environment dahlia \\\n        --start 2023-01-06T07:30:00-0800 \\\n        --end 2023-01-06T17:00:00-0800 \\\n        --cuwb-data ./output/uwb_data/uwb-dahlia-20230106-153000-20230107-010000.pkl \\\n        --tray-carry-model ./output/models/tray_carry_model_v1.pkl\n\n\n### Train Tray Detection Model\nThe tray detection model is a simple RandomForest model. It\'s used by many of the available methods in the library.\n\n1. Download/create [ground_truth_tray_carry.csv](https://docs.google.com/spreadsheets/d/1NLQ_7Cj432T1AXFcbKLX3P6LGGGRAklxMTjtBYS_xhA/edit?usp=sharing) to `./downloads/ground_truth_tray_carry.csv`\n```\n    curl -L \'https://docs.google.com/spreadsheets/d/1NLQ_7Cj432T1AXFcbKLX3P6LGGGRAklxMTjtBYS_xhA/export?exportFormat=csv\' --output ./downloads/ground_truth_tray_carry.csv\n```\n\n2. Generate pickled groundtruth features dataframe from ground_truth_tray_carry.csv\n\nThis will download data from Honeycomb and prepare it for the next step of feeding it into a model for training.\n\n```\n    process_cuwb_data \\\n        generate-tray-carry-groundtruth \\\n        --groundtruth-csv ./downloads/ground_truth_tray_carry.csv\n```\n\n3. Train and pickle Tray Carry Detection Model using pickled groundtruth features\n\n```\n    process_cuwb_data \\\n        train-tray-carry-model \\\n        --groundtruth-features ./output/groundtruth/2021-05-13T12:53:26_tray_carry_groundtruth_features.pkl\n```\n\n### Infer Tray Carries\n\n1. Infer Tray Interactions using a pickled Tray Carry Detection Model\n    1. Use the model you\'ve trained by following the steps to **Train Tray Detection Model**\n    2. Or, download the latest model:\n```\n    curl -L \'https://drive.google.com/uc?export=download&id=1_veyjLdAa8Fq7eYeT9GLdkcS6_VY0FLX\' --output ./output/models/tray_carry_model_v1.pkl\n```   \n\n### Infer Tray Interaction \n\nThis outputs a list of tray carries (CARRY FROM SHELF / CARRY TO SHELF / CARRY UNKNOWN / etc.) and describe the person, the material, the length of the carry, and median distance between the nearest person and tray over the course of the event\n\n     process_cuwb_data \\\n         infer-tray-interactions \\\n         --environment greenbrier \\\n         --start 2021-04-20T9:00:00-0500 \\\n         --end 2021-04-20T9:05:00-0500 \\\n         --tray-carry-model ./output/models/2021-05-13T14:49:32_tray_carry_model.pkl \\\n         --cuwb-data ./output/uwb_data/uwb-greenbrier-20210420-140000-20210420-140500.pkl\n        \n    (or, instead of --cuwb-datam, use) --motion-feature-data ./output/feature_data/motion-features-greenbrier-20210527-141300-20210527-141500.pkl\n    (optionally, supply tray positions/centroids. Note, these locations should ALWAYS be provided if attempting to infer tray interactions on a partial window of classroom time.) --tray-positions-csv ./output/locations/2023-01-19T15:57:12_tray_centroids.csv\n\n#### Supply Pose Track Inference to Tray Interaction Inference\n\nUse Pose Tracks when determining nearest person to tray carry events.\n\nPose Inferences need to be sourced in a local directory. The pose directory can be supplied via CLI options.\n   \n     process_cuwb_data \\\n         infer-tray-interactions \\\n         --environment greenbrier \\\n         --start 2021-04-20T9:00:00-0500 \\\n         --end 2021-04-20T9:05:00-0500 \\\n         --tray-carry-model ./output/models/2021-05-13T14:49:32_tray_carry_model.pkl \\\n         --cuwb-data ./output/uwb_data/uwb-greenbrier-20210420-140000-20210420-140500.pkl \\\n         --pose-inference-id 3c2cca86ceac4ab1b13f9f7bfed7834e\n\n### Infer Tray Events\n\nThis is a more standardized version/output of Tray Interactions. It\'s the format used by the Material Events API. It\'s input includes the TrayInteractions CSV from **Infer Tray Interaction**\n\n*Note, `time_zone` is a required parameter. It\'s used to construct strings with times that will be read by end users. We will not default this to timezone that may be invalid.*\n\n     process_cuwb_data \\\n         infer-tray-events \\\n         --environment dahliasf \\\n         --tray-interactions ./output/inference/tray_interactions/2023-01-23T15:28:30_tray_interactions.csv \\\n         --time_zone US/Pacific\n\n### Infer Material Events\n\nThis generates a list of "complete" material events. A complete material event starts with a Carry From Shelf and ends with a Carry To Shelf. The Material Events output also includes a list of cameras that best capture the arc of the material event. \n\n*Note, `time_zone` is a required parameter. It\'s used to construct strings with times that will be read by end users. We will not default this to timezone that may be invalid.*\n\n     process_cuwb_data \\\n         infer-material-events \\\n         --environment dahliasf \\\n         --tray-events ./output/inference/tray_events/2023-01-23T22:05:02_tray_events.csv \\\n         --timezone US/Pacific\n',
    'author': 'Theodore Quinn',
    'author_email': 'ted.quinn@wildflowerschools.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WildflowerSchools/wf-process-cuwb-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
