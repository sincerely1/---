import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {

    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'Home',
      component: () => import('@/views/home/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: 'Profile', icon: 'user', noCache: true }
      }
    ]
  }
]
export const asyncRoutes = [
  {
    path: '/permission',
    component: Layout,
    redirect: '/permission/role',
    name: 'Permission',
    meta: {
      title: '用户和权限管理',
      icon: 'lock',
      roles: ['admin']
    },
    children: [
      {
        path: 'user',
        component: () => import('@/views/permission/user'),
        name: 'UserManagement',
        meta: {
          title: '用户管理管理'
        }
      }
    ]
  },
  {
    path: '/lesson',
    component: Layout,
    name: 'Lesson',
    meta: {
      title: '课程列表',
      icon: 'lesson-manager',
      roles: ['teacher', 'student']
    },
    children: [
      {
        path: '/student/select',
        component: () => import('@/views/lesson/student/has_select'),
        name: 'select',
        meta: {
          title: '学生已选课',
          icon: 'select-lesson',
          roles: ['student']
        }
      },
      {
        path: '/student/nosel',
        component: () => import('@/views/lesson/student/can_select'),
        name: 'noselect',
        meta: {
          title: '学生可选课程',
          icon: 'select-lesson',
          roles: ['student']
        }
      },
      {
        path: '/teacher/course',
        component: () => import('@/views/lesson/teacher/manageCourse'),
        name: 'Course',
        meta: {
          title: '教师课程管理',
          icon: 'select-lesson',
          roles: ['teacher']
        }
      },
      {
        path: '/teacher/course_data',
        component: () => import('@/views/lesson/teacher/uploadCourseData'),
        name: 'CourseData',
        meta: {
          title: '教师课程数据管理',
          icon: 'select-lesson',
          roles: ['teacher']
        }
      }
    ]
  },
  {
    path: '/charts',
    component: Layout,
    name: 'Charts',
    redirect: '/charts/analysis-list',
    meta: {
      title: '可视化分析',
      icon: 'chart',
      roles: ['teacher', 'student']
    },
    children: [
      {
        path: 'analysis-list',
        component: () => import('@/views/charts/course_list'),
        name: '分析完成课程列表',
        meta: {
          title: '完成分析课程列表',
          roles: ['student', 'teacher']
        }
      },
      {
        path: 'student-dashboard',
        component: () => import('@/views/charts/student/dashboard'),
        name: 'Student Dashboard',
        meta: {
          title: 'Dashboard',
          roles: ['student']
        }
      },
      {
        path: 'student-return-data',
        component: () => import('@/views/charts/student/return_analysis'),
        name: 'Student Return Data',
        meta: {
          title: '返回结果分析',
          roles: ['student']
        }
      },
      {
        path: 'student-question-type',
        component: () => import('@/views/charts/student/question_type_analysis'),
        name: 'Student Question Type Data',
        meta: {
          title: '不同题目类型分析',
          roles: ['student']
        }
      },
      {
        path: 'student-knowledge',
        component: () => import('@/views/charts/student/knowledge-analysis/index'),
        name: 'Student Knowledge',
        meta: {
          title: '知识点对比分析',
          roles: ['student']
        },
        children: [
          {
            path: 'student-knowledge-commit',
            component: () => import('@/views/charts/student/knowledge-analysis/knowledge_commit'),
            name: 'Student knowledge_commit',
            meta: {
              title: '知识点提交次数分析',
              roles: ['student']
            }
          },
          {
            path: 'student-knowledge-first-accept',
            component: () => import('@/views/charts/student/knowledge-analysis/knowledge_firstaccept'),
            name: 'Student knowledge_first_accept',
            meta: {
              title: '知识点首次通过分析',
              roles: ['student']
            }
          },
          {
            path: 'student-knowledge-pass',
            component: () => import('@/views/charts/student/knowledge-analysis/knowledge_pass'),
            name: 'Student knowledge_pass',
            meta: {
              title: '知识点通过分析',
              roles: ['student']
            }
          }
        ]

      },

      {
        path: 'student-level',
        component: () => import('@/views/charts/student/level_analysis/index'),
        name: 'Student Level',
        meta: {
          title: '难度对比分析',
          roles: ['student']
        },
        children: [
          {
            path: 'student-level-accept',
            component: () => import('@/views/charts/student/level_analysis/level_accept_analysis'),
            name: 'Student Level Accept Data',
            meta: {
              title: '难度通过分析',
              roles: ['student']
            }
          },
          {
            path: 'student-level-commit',
            component: () => import('@/views/charts/student/level_analysis/level_commit_analysis'),
            name: 'Student Level Commit Data',
            meta: {
              title: '难度提交分析',
              roles: ['student']
            }
          },
          {
            path: 'student-level-code',
            component: () => import('@/views/charts/student/level_analysis/level_code_analysis'),
            name: 'Student Level Code Data',
            meta: {
              title: '难度代码质量分析',
              roles: ['student']
            }
          }
        ]

      },
      {
        path: 'teacher-dashboard',
        component: () => import('@/views/charts/teacher/dashboard'),
        name: 'Teache Dashboard',
        meta: {
          title: 'Dashboard',
          roles: ['teacher']
        }
      },
      {
        path: 'teacher-compare',
        component: () => import('@/views/charts/teacher/course_compare'),
        name: 'Teache Compare',
        meta: {
          title: '课程对比分析',
          roles: ['teacher']
        }
      },
      {
        path: 'teacher-ability-count',
        component: () => import('@/views/charts/teacher/ability_count_analysis'),
        name: 'Student Count Ability Data',
        meta: {
          title: '胜任力统计分析',
          roles: ['teacher']
        }
      },
      {
        path: 'teacher-homework-commit',
        component: () => import('@/views/charts/teacher/homework_excle'),
        name: 'Teacher Homework Data',
        meta: {
          title: '作业提交分析',
          roles: ['teacher']
        }
      },
      {
        path: 'teacher-detail',
        component: () => import('@/views/charts/teacher/detail-analysis/index'),
        name: 'Teacher Analysis Detail',
        meta: {
          title: '详细分析',
          roles: ['teacher']
        },
        children: [
          {
            path: 'teacher-question-commit-start',
            component: () => import('@/views/charts/teacher/detail-analysis/accept_time_analysis'),
            name: 'Student Start Commit Data',
            meta: {
              title: '开始答题时间分析',
              roles: ['teacher']
            }
          },
          {
            path: 'teacher-question-return-sum',
            component: () => import('@/views/charts/teacher/detail-analysis/return_summary'),
            name: 'Student Sum Return Data',
            meta: {
              title: '提交返回分析',
              roles: ['teacher']
            }
          },
          {
            path: 'teacher-knowledge-summary',
            component: () => import('@/views/charts/teacher/detail-analysis/knowledge_summary_analysis'),
            name: 'Teacher Sun Knowledge Data',
            meta: {
              title: '知识点统计分析',
              roles: ['teacher']
            }
          },
          {
            path: 'teacher-level-summary',
            component: () => import('@/views/charts/teacher/detail-analysis/level_summary_analysis'),
            name: 'Teacher Sun Level Data',
            meta: {
              title: '难度统计分析',
              roles: ['teacher']
            }
          },
          {
            path: 'teacher-type-summary',
            component: () => import('@/views/charts/teacher/detail-analysis/type_summary_analysis'),
            name: 'Teacher Sun type Data',
            meta: {
              title: '题型统计分析',
              roles: ['teacher']
            }
          }
        ]

      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'hash', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})
const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
