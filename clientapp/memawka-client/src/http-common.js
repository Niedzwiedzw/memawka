import axios from 'axios'
import jscookie from 'js-cookie'

export default axios.create({
  baseURL: 'http://165.227.133.227:8000',
  headers: {
    'Authorization': 'token ' + jscookie.get('meme-token')
  }
})
