'''
Created on May 2015

@author: Arthur Glowacki, Argonne National Laboratory

Copyright (c) 2013, Stefan Vogt, Argonne National Laboratory
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this
        list of conditions and the following disclaimer in the documentation and/or
        other materials provided with the distribution.
    Neither the name of the Argonne National Laboratory nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
'''
from handlers import HandlerBase


class Route:
	def __init__(self, function_name, http_method, controller, path=None):
		path = Route.__getPath(path, function_name)

		self.name = function_name
		self.action = function_name
		self.controller = controller
		self.method = http_method
		self.path = path

	@staticmethod
	def __getPath(path, function_name):
		if path is None:
			return '/%s' % function_name
		return path


	@staticmethod
	def createRoutes(function_name, http_method, controller, includeOptionsHTTPMethodForPath=False, path=None):
		routes = [];

		routes.append(Route(function_name, http_method, controller, path));
		if includeOptionsHTTPMethodForPath:
			path = Route.__getPath(path, function_name)
			routes.append(Route(HandlerBase.ADD_OPTIONS_FUNCTION_NAME, 'OPTIONS', controller, path))

		return routes;