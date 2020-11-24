
import i18n


def adjustment_Modal(params, date):
    modal = {
        'title': {
            'type': 'plain_text',
            'text': "Schedule adjustment"
        },
        'submit': {
            'type': 'plain_text',
            'text': "Adjust"
        },
        'blocks': [
            {
                'type': 'input',
                'block_id': 'title',
                'element': {
                    'type': 'plain_text_input',
                    'action_id': 'meeting_title',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': 'Meeting Title'
                    }
                },
                'label': {
                    'type': 'plain_text',
                    'text': 'Title'
                }
            },
            {
                'type': 'section',
                'block_id': 'meeting_duration',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Duration'
                },
                'accessory': {
                    'action_id': 'duration',
                    'type': 'static_select',
                    'options': [
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '15 minutes'
                            },
                            'value': '15'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '30 minutes'
                            },
                            'value': '30'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '1 hour'
                            },
                            'value': '60'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '1.5 hour'
                            },
                            'value': '90'
                        }
                    ]
                }
            },
            {
                'type': 'section',
                'block_id': 'date',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Pick a meeting date'
                },
                'accessory': {
                    'type': 'datepicker',
                    'action_id': 'meeting_date',
                    'initial_date': date,
                    'placeholder': {
                        'type': 'plain_text',
                        'text': 'Select a date'
                    }
                }
            },
            {
                'type': 'section',
                'block_id': 'floor',
                'text': {
                    'type': 'mrkdwn',
                    'text': i18n.t('MESSAGE_GUEST_REGISTER_LABEL_MEETING_FLOOR')
                },
                'accessory': {
                    'action_id': 'meeting_floor',
                    'type': 'static_select',
                    'options': [
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '18{postfix}'.format(postfix=i18n.t('MESSAGE_GUEST_REGISTER_LABEL_FLOOR_POSTFIX'))
                            },
                            'value': '18'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '25{postfix}'.format(postfix=i18n.t('MESSAGE_GUEST_REGISTER_LABEL_FLOOR_POSTFIX'))
                            },
                            'value': '25'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '43{postfix}'.format(postfix=i18n.t('MESSAGE_GUEST_REGISTER_LABEL_FLOOR_POSTFIX'))
                            },
                            'value': '43'
                        }
                    ]
                }
            },
            {
                'type': 'section',
                'block_id': 'mandatory_users',
                'text': {
                    'type': "mrkdwn",
                    'text': "Mandatory Users"
                },
                'accessory': {
                    'action_id': "users",
                    'type': "multi_users_select",
                    'placeholder': {
                        'type': "plain_text",
                        'text': "Select users"
                    }
                }
            },
            {
                'type': 'section',
                'block_id': 'optional_users',
                'text': {
                    'type': "mrkdwn",
                    'text': "Optional Users"
                },
                'accessory': {
                    'action_id': "users",
                    'type': "multi_users_select",
                    'placeholder': {
                        'type': "plain_text",
                        'text': "Select Optional users"
                    }
                }
            }
        ],
        'type': 'modal',
        'private_metadata': params['channel'] + '~~~' + params['ts'] + '~~~' + params['data']['lang'],
        'callback_id': 'T_Meeting_Arrangement_Yes',
        'notify_on_close': True
    }
    return modal
