#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from java.lang import Exception
import json

from pivotaltracker.Client import Client
client = Client(pivotaltrackerServer)

data = { 'count': 0, 'error' :'', 'types': [], 'stories':[] }

try:
    if pivotaltrackerServer != None:
        if stories != None and len(stories) > 0:
            types = {}
            for story_id in stories:
                story = client.getStory(str(project_id), str(story_id))
                if story['story_type'] in types:
                    types[story['story_type']] = types[story['story_type']] + 1
                else:
                    types[story['story_type']] = 1
                data['count'] += 1
                data['stories'].append(story)
            for l in types:
                data['types'].append({'type':l, 'count':types[l]})

except Exception as exception:
    logger.error(exception.getMessage())
    data['error'] = exception.getMessage()