from datetime import datetime, timedelta
import pytz

pod_test_data = {
    'name': 'pod1',
    'image': 'image',
    'start_time': (datetime.now() - timedelta(days=3)).replace(tzinfo=pytz.UTC),
    'labels': {'team': 'team1'}
}


expected_eval_result = {
    'pod': 'pod1',
    'rule_evaluation': [
        {'name': 'image_prefix', 'valid': False},
        {'name': 'team_label_present', 'valid': True},
        {'name': 'recent_start_time', 'valid': True}
    ]
}