import axios from 'axios'

let validateToken = (accessToken) => {
  axios(
    {
      method: 'post',
      url: 'http://127.0.0.1:8000/api-token-verify/',
      data: {
        token: accessToken
      }
    }
  ).then((response) => {
      return response.data.token === accessToken
    }
  ).catch((response) => {
      return false
    }
  )
}

export { validateToken }
