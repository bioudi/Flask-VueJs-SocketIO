<template>
  <div class="columns is-multiline is-gapless" style="width:100%;">
    <div class="column is-12">
      <table class="table is-bordered is-striped is-narrow">
            <thead>
              <th>Date Ordre</th>
              <th>Nombre Actions</th>
              <th>Prix Action</th>
              <th>Type d'ordre</th>
            </thead>
            <tfoot></tfoot>
            <tbody>
              <tr v-for="ordre in displayedData">
                <td>{{ordre.date_ordre}}</td>
                <td>{{ordre.nbre_actions}}</td>
                <td>{{ordre.prix_action}}</td>
                <td>{{ordre.type_ordre}}</td>
              </tr>
            </tbody>
          </table>
          <div class="columns">
            <div class="column is-offset-1">
              <a class="button is-primary is-outlined" disabled v-show="!isPrecedent">Precedent</a>
              <a class="button is-primary is-outlined" @click="prev()" v-show="isPrecedent">Precedent</a>
            </div>
            <div class="column">
              <h3>{{currentPage}} de {{countPages}} pages</h3>
            </div>
            <div class="column">
              <a class="button is-primary is-outlined" @click="next()" disabled v-show="!isNext">Suivant</a>
              <a class="button is-primary is-outlined" @click="next()" v-show="isNext">Suivant</a>
            </div>
          </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'paginate-table',
  props:['data'],
  data () {
    return {
      itemPerPage:3,
      currentPage:1,
      isPrecedent:true,
      isNext:true,
    }
  },
  computed:{
    countPages:function(){
      return Math.ceil(this.data.length/this.itemPerPage);
    },
    displayedData:function(){
      return this.data.slice(this.itemPerPage*this.currentPage-this.itemPerPage,this.itemPerPage*this.currentPage);
    }
  },
  methods:{
    next(){
      if(this.currentPage<this.countPages)
      {
        this.currentPage++;
        this.isPrecedent = true;
      }
      if(this.currentPage==this.countPages)
        this.isNext = false;
    },
    prev(){
      if(this.currentPage>1)
      {
        this.currentPage--;
        this.isNext = true;
      }
      if(this.currentPage==1)
        this.isPrecedent = false;
    }
  },
  mounted:function(){
    Event.listen('code',()=>{
      this.currentPage=1;
    })
  }
}
</script>

<style scoped>

</style>
