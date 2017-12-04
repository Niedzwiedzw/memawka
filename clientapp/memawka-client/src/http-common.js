import axios from 'axios'
import jscookie from 'js-cookie'

export default axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Authorization': 'token ' + jscookie.get('meme-token')
  }
})

// let validateToken = function () {
//   axios(
//     {
//       method: 'post',
//       url: 'http://127.0.0.1:8000/api-token-verify/',
//       data: {
//         token: jscookie.get('meme-token')
//       }
//     }
//   ).then((response) => {
//
//       console.log('cookie', jscookie.get('meme-token'))
//       return response.data.token === accessToken
//     }
//   ).catch((response) => {
//       console.log('token is invalid')
//
//       console.log('cookie', jscookie.get('meme-token'))
//       return false
//     }
//   )
// }
//
