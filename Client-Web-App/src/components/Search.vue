<template>
  <div class="columns">
    <div class="column">
      <nav class="panel">
        <p class="panel-heading">
          Chercher Societe
        </p>
        <div class="panel-block">
          <p class="control has-icons-left">
            <input class="input is-small" type="text" placeholder="Code Societe ..." v-model="code">
            <span class="icon is-small is-left">
              <i class="fa fa-search"></i>
            </span>
          </p>
          <div class="column">
            <button @click="sendCode()" class="button is-primary">
              Rechercher
            </button>
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: 'search',
  data () {
    return {
        code:''
    }
  },
  methods:{
    sendCode(){
      if(this.code){
        Event.fire('code',this.code);
      }
    }
  },
  created:function(){
    Event.listen('code1',function(){
      this.sendCode();
    }.bind(this))
  }
}
</script>

<style scoped>
  .panel{
    margin-top: 20px;
  }
</style>
