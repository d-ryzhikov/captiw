-- Test static data retrieval.
wrk.path = '/static/data'
wrk.method = 'GET'

i = 0

request = function()
    req = wrk.format('GET', '/static/data' .. i % 5)
    i = i + 1
    return req
end
