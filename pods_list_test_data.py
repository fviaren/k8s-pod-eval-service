from datetime import datetime, timedelta

pods_list_test_data = [
    {
        'name': 'pod1',
        'image': 'image',
        'start_time': (datetime.now() - timedelta(days=3)),
        'labels': {'team': 'team1'}
    },
    {
        'name': 'pod2',
        'image': 'bitnami/3232',
        'start_time': (datetime.now() - timedelta(days=8)),
        'labels': {'label2': 'foo'}
    },
    {
        'name': 'pod3',
        'image': 'bitnami/rere',
        'start_time': (datetime.now() - timedelta(days=2)),
        'labels': {'team': ''}
    }
]

expected_eval_result = [
    {
        'pod': 'pod1',
        'rule_evaluation': [
            {'name': 'image_prefix', 'valid': False},
            {'name': 'team_label_present', 'valid': True},
            {'name': 'recent_start_time', 'valid': True}
        ]
    },
    {
        'pod': 'pod2',
        'rule_evaluation': [
            {'name': 'image_prefix', 'valid': True},
            {'name': 'team_label_present', 'valid': False},
            {'name': 'recent_start_time', 'valid': False}
        ]
    },
    {
        'pod': 'pod3',
        'rule_evaluation': [
            {'name': 'image_prefix', 'valid': True},
            {'name': 'team_label_present', 'valid': False},
            {'name': 'recent_start_time', 'valid': True}
        ]
    },
]

