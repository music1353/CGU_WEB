import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login'
import Signup from '@/components/Signup'
import UserIndex from '@/views/User/UserIndex'
import UserAward from '@/views/User/UserAward'
import UserGame from '@/views/User/UserGame'
import AdminIndex from '@/views/Admin/AdminIndex'
import AdminUsersManage from '@/views/Admin/AdminUsersManage'
import AdminGiftRecord from '@/views/Admin/AdminGiftRecord'
import AdminFeedback from '@/views/Admin/AdminFeedback'
import AdminDataCenter from '@/views/Admin/AdminDataCenter'
import ParentIndex from '@/views/Parent/ParentIndex'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Login
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/signup',
      name: 'Signup',
      component: Signup
    },
    {
      path: '/user/index',
      name: 'UserIndex',
      component: UserIndex
    },
    {
      path: '/user/game/:gameNameEN',
      name: 'UserGame',
      component: UserGame
    },
    {
      path: '/user/award',
      name: 'Award',
      component: UserAward
    },
    {
      path: '/admin/index',
      name: 'Index',
      component: AdminIndex
    },
    {
      path: '/admin/usersManage',
      name: 'AdminUsersManage',
      component: AdminUsersManage
    },
    {
      path: '/admin/giftRecord',
      name: 'AdminGiftRecord',
      component: AdminGiftRecord
    },
    {
      path: '/admin/feedback',
      name: 'AdminFeedback',
      component: AdminFeedback
    },
    {
      path: '/admin/dataCenter',
      name: 'AdminDataCenter',
      component: AdminDataCenter
    },
    {
      path:'/parent/index',
      component: ParentIndex
    }
  ]
})
