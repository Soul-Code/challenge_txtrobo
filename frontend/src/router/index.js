import Vue from 'vue'
import Router from 'vue-router'
import Chat from '../components/chat/chat'
import Chatroom from '../components/chatroom/chatroom'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/chatroom'
    },
    {
      path: '/chatroom',  // 聊天打字界面
      component: Chatroom
      // children: [
      //   {
      //     path: 'user',
      //     component: ChatroomUser
      //   }
      // ]
    },
    {
      path: '/chat',  // 第一栏：微信
      component: Chat
    }]
})
