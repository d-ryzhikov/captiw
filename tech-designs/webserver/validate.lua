-- Test json body validation.
math.randomseed(42)

method = 'POST'
path = '/validate'
headers = {["Content-Type"] = 'application/json'}

invalidBody = '{"addr": "blabla", "logined": "kek"}'
validBody = '{"addr": "127.0.0.1", "login": "foo", "password": "bar"}'

request = function()
    if math.random() > 0.5 then
        body = invalidBody
    else
        body = validBody
    end
    return wrk.format(method, path, headers, body)
end
