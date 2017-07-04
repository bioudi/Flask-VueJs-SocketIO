// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Search from './components/Search.vue'
import Societe from './components/societeGrid.vue'
import router from './router'


Vue.config.productionTip = false

window.Event = new class{
  constructor() {
    this.vue = new Vue()
  }

  fire(event,data = null){
    this.vue.$emit(event,data);
  }

  listen(event,callback)
  {
    this.vue.$on(event,callback);
  }
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  data:{
    societes : []
  },
  router,
  components: { Search,Societe },
  created:function(){
    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('connect',function(){
      socket.emit('first-connect','A user has connected');
    })
    setInterval(function(){
      socket.emit('ping');
      console.log('is the session alive ?')
    }, 10000);
    socket.on('pong',function(){
      console.log('session is alive')
    })
    socket.on('data-arrived',function(data){
      this.societes = data;
      console.log(this.societes);
      Event.fire('code1')
    }.bind(this))
    Event.listen('code',function(code){
      this.sendCodeToSociete(code)
    }.bind(this));
    },
    methods:{
      sendCodeToSociete(code){
        this.societes.forEach(function(element){
          if(element.code_societe == code){
            Event.fire('societe',element)
          }
        });
      }
    }
})
