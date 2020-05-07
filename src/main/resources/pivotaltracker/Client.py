#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from xlrelease.HttpRequest import HttpRequest
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory

class Client(object):

    def __init__(self, httpConnection):
        self.httpConnection = httpConnection
        self.content_type = 'application/json'
        self.encoding = 'utf-8'
        self.params = {'url': httpConnection['url'], 'proxyHost': httpConnection['proxyHost'], 'proxyPort': httpConnection['proxyPort'], 'proxyUsername': httpConnection['proxyUsername'], 'proxyPassword': httpConnection['proxyPassword']}
        self.headers = {'X-TrackerToken': httpConnection['apitoken'] }
        self.logger = LoggerFactory.getLogger('com.xebialabs.pivotaltracker-plugin')

    def testServer(self):
        response = HttpRequest(self.params).get('/me', content=None, headers=self.headers)
        self.logger.info(response.response)
        return

    def _postRequest(self, url, data):
        encoded_data = json.dumps(data).encode(self.encoding)
        response = HttpRequest(self.params).post(url, encoded_data, contentType=self.content_type, headers=self.headers)
        return response

    def _putRequest(self, url, data):
        encoded_data = json.dumps(data).encode(self.encoding)
        response = HttpRequest(self.params).put(url, encoded_data, contentType=self.content_type, headers=self.headers)
        return response

    def createStory(self, project_id, name, description, story_type, current_state, labels):
        story = {}
        url = '/projects/%(p)s/stories' % { 'p': project_id }
        data = {
            'name': name
        }
        if description != None:
            data['description'] = description
        if story_type != None:
            data['story_type'] = story_type
        if current_state != None:
            data['current_state'] = current_state
        if labels != None:
            data['labels'] = [ l for l in labels ]

        response = self._postRequest(url, data)
        obj = json.loads(response.response)
        for (k,v) in obj.items():
            story[k] = json.dumps(v)
        return story

    def updateStory(self, project_id, story_id, name, description, story_type, current_state, labels):
        story = {}
        url = '/projects/%(p)s/stories/%(s)s' % { 'p': project_id, 's' :  story_id }
        data = {}
        if name != None:
            data['name'] = name
        if description != None:
            data['description'] = description
        if story_type != None:
            data['story_type'] = story_type
        if current_state != None:
            data['current_state'] = current_state
        if labels != None:
            data['labels'] = [ l for l in labels ]

        response = self._putRequest(url, data)
        obj = json.loads(response.response)
        for (k,v) in obj.items():
            story[k] = json.dumps(v)
        return story