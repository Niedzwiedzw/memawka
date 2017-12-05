import axios from 'axios'
import jscookie from 'js-cookie'

export default axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Authorization': 'token ' + jscookie.get('meme-token')
  }
})
