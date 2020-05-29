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
import urllib
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory

from xlrelease.HttpRequest import HttpRequest
from util import error

class Client(object):

    def __init__(self, httpConnection, task_reporting_api = None, task = None):
        self.httpConnection = httpConnection
        self.content_type = 'application/json'
        self.encoding = 'utf-8'
        self.params = {'url': httpConnection['url'], 'proxyHost': httpConnection['proxyHost'], 'proxyPort': httpConnection['proxyPort'], 'proxyUsername': httpConnection['proxyUsername'], 'proxyPassword': httpConnection['proxyPassword']}
        self.headers = {'X-TrackerToken': httpConnection['apitoken'] }
        self.logger = LoggerFactory.getLogger('com.xebialabs.pivotaltracker-plugin')
        self.task_reporting_api = task_reporting_api
        self.task = task

    def testServer(self):
        response = HttpRequest(self.params).get('/me', content=None, headers=self.headers)
        self.logger.info(response.response)
        return

    def _getRequest(self, url):
        response = HttpRequest(self.params).get(url, content=None, contentType=self.content_type, headers=self.headers)
        return response

    def _postRequest(self, url, data):
        encoded_data = json.dumps(data).encode(self.encoding)
        response = HttpRequest(self.params).post(url, encoded_data, contentType=self.content_type, headers=self.headers)
        return response

    def _putRequest(self, url, data):
        encoded_data = json.dumps(data).encode(self.encoding)
        response = HttpRequest(self.params).put(url, encoded_data, contentType=self.content_type, headers=self.headers)
        return response

    def _createPlanRecord(self, story):
        if self.task_reporting_api and self.task:
            planRecord = self.task_reporting_api.newPlanRecord()
            planRecord.targetId = self.task.id
            planRecord.ticket = str(story['id'])
            planRecord.title = story['name']
            planRecord.ticketType = story['story_type']
            planRecord.creationDate = story['created_at']
            planRecord.updatedDate = story['updated_at']
            planRecord.serverUrl = self.httpConnection['url']
            planRecord.serverUser = self.httpConnection['username']
            planRecord.ticket_url = story['url']
            planRecord.status = story['current_state']
            self.task_reporting_api.addRecord(planRecord, True)
            self.logger.info('Created Plan record')

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
        if response.status == 200:
            obj = json.loads(response.response)
            for (k,v) in obj.items():
                story[k] = json.dumps(v)
            self._createPlanRecord(obj)
        else:
            error("Failed to create story in PivotalTracker.", response)
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
        if response.status == 200:
            obj = json.loads(response.response)
            for (k,v) in obj.items():
                story[k] = json.dumps(v)
            self._createPlanRecord(obj)
        else:
            error("Failed to update story in PivotalTracker.", response)
        return story

    def getStories(self, project_id, with_label, with_story_type, with_state, after_story_id, before_story_id):
        stories={}
        url = '/projects/%(p)s/stories' % { 'p': project_id }
        params = {}
        if (with_label != None) and (with_label != '') :
            params['with_label'] = with_label.encode('utf-8')
        if with_story_type != None:
            params['with_story_type'] = with_story_type
        if with_state != None:
            params['with_state'] = with_state
        if (after_story_id != None) and (after_story_id !=''):
            params['after_story_id'] = after_story_id
        if (before_story_id != None) and (before_story_id != ''):
            params['before_story_id'] = before_story_id
        url += '?%(p)s' % { 'p' : urllib.urlencode(params) }
        response = self._getRequest(url)
        if response.status == 200:
            obj = json.loads(response.response)
            for l in obj:
                stories[l['id']] = l['name']
        else:
            error("Failed to get stories from PivotalTracker.", response)
        return stories


    def getStoriesForRelease(self, project_id, release_id):
        stories = {}
        url = '/projects/%(p)s/releases/%(r)s/stories' % { 'p': project_id, 'r': release_id }
        response = self._getRequest(url)
        if response.status == 200:
            obj = json.loads(response.response)
            for s in obj:
                stories[s['id']] = s['name']
        else:
            error("Failed to get stories from PivotalTracker.", response)
        return stories

    def getStory(self, project_id, story_id):
        obj = None
        url = '/projects/%(p)s/stories/%(s)s' % { 'p': project_id, 's': story_id }
        response = self._getRequest(url)
        if response.status == 200:
            obj = json.loads(response.response)
        else:
            error("Failed to get story from PivotalTracker.", response)
        return obj