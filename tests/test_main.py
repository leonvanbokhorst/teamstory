import unittest
from unittest import mock
import sys
import types

# Provide a dummy openai module when the real package isn't available.
if 'openai' not in sys.modules:
    sys.modules['openai'] = types.SimpleNamespace(
        ChatCompletion=types.SimpleNamespace(create=lambda *a, **k: None)
    )

import src.main as main

class GenerateStoryTests(unittest.TestCase):
    def setUp(self):
        # Keep a copy of the original context
        self.original_context = {k: list(v) for k, v in main.context.items()}
        for v in main.context.values():
            v.clear()

    def tearDown(self):
        # Restore original context
        for k in main.context.keys():
            main.context[k] = list(self.original_context[k])

    def test_no_context(self):
        story = main.generate_story()
        self.assertEqual(story, "No stories yet. Add context via /admin.")

    @mock.patch('main.litellm.completion')
    def test_litellm_success(self, mock_create):
        # Populate minimal context
        main.context['projects'].append('proj1')
        main.context['students'].append('stud1')
        main.context['educators'].append('edu1')
        main.context['techniques'].append('tech1')
        main.context['results'].append('res1')

        class FakeChoice:
            def __init__(self, content):
                self.message = {"content": content}
        mock_create.return_value = type('obj', (), {'choices': [FakeChoice('Custom story.')]})

        story = main.generate_story()
        self.assertEqual(story, 'Custom story.')

    @mock.patch('main.random.choice', side_effect=lambda seq: seq[0])
    @mock.patch('main.litellm.completion', side_effect=Exception('fail'))
    def test_litellm_failure(self, mock_create, mock_choice):
        main.context['projects'].append('proj1')
        main.context['students'].append('stud1')
        main.context['educators'].append('edu1')
        main.context['techniques'].append('tech1')
        main.context['results'].append('res1')

        story = main.generate_story()
        expected = "stud1 and edu1 are exploring tech1 in proj1, leading to res1."
        self.assertEqual(story, expected)

if __name__ == '__main__':
    unittest.main()
