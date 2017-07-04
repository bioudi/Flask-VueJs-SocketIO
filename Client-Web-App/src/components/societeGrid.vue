<template>
  <div class="columns" v-show="show">
  <div class="column">
    <nav class="panel">
      <p class="panel-heading">
        Infos sur la societe
      </p>
      <div class="panel-block">
        <div class="columns is-multiline is-gapless" style="width:100%;">
          <div class="column is-12">
            <table class="table is-bordered is-striped is-narrow">
                  <thead>
                    <th>Code</th>
                    <th>Nom</th>
                  </thead>
                  <tfoot></tfoot>
                  <tbody>
                    <tr>
                      <td>{{societe.code_societe}}</td>
                      <td>{{societe.nom_societe}}</td>
                    </tr>
                  </tbody>
                </table>
          </div>
          <div class="column is-12">
            <table class="table is-bordered is-striped is-narrow">
                  <thead>
                    <th>Actions Vente</th>
                    <th>Actions Achat</th>
                    <th>Prix Moyen Vente</th>
                    <th>Prix Moyen Achat</th>
                    <th>Estimation</th>
                  </thead>
                  <tfoot></tfoot>
                  <tbody>
                    <tr>
                      <td>{{totalAchat}}</td>
                      <td>{{totalVente}}</td>
                      <td>{{prixMoyenVente}}</td>
                      <td>{{prixMoyenAchat}}</td>
                      <td>-</td>
                    </tr>
                  </tbody>
                </table>
          </div>
        </div>
      </div>
    </nav>
  </div>
  <div class="column">
    <nav class="panel">
      <p class="panel-heading">
        Ordre Societe
      </p>
      <div class="panel-block">
        <paginate-table :data="allOrdres"></paginate-table>
      </div>
    </nav>
  </div>
</div>
</template>

<script>
import PaginateTable from './PaginateTable.vue'
import axios from 'axios';
export default {
  name: 'societe',
  data () {
    return {
      societe:{
          "code_societe": null,
          "nom_societe": null,
          "ordre_achat": [],
          "ordre_vente": []
      },
      show:false
    }
  },
  created: function ()
  {
      Event.listen('societe',(societe=>{this.societe=societe;console.log('The societe Updated');this.show=true;}))
  },
  computed:{
    allOrdres(){
      return this.societe.ordre_achat.concat(this.societe.ordre_vente);
    },
    totalVente(){
      let tot = 0;
      this.societe.ordre_vente.forEach((element=>tot+=parseInt(element.nbre_actions)))
      return tot;
    },
    totalAchat(){
      let tot = 0;
      this.societe.ordre_achat.forEach((element=>tot+=parseInt(element.nbre_actions)))
      return tot;
    },
    prixMoyenVente(){
      let tot=0;
      this.societe.ordre_vente.forEach((element=>{
        tot+=parseFloat(element.prix_action.replace(',', '.').replace(/\s/g, ''));
      }))
      return Math.round(tot/this.totalVente)
    },
    prixMoyenAchat(){
      let tot=0;
      this.societe.ordre_achat.forEach((element=>{
        tot+=parseFloat(element.prix_action.replace(',', '.').replace(/\s/g, ''));
      }))
      return Math.round(tot/this.totalAchat)
    }
  },
  components:{PaginateTable}
}
</script>

<style scoped>

</style>
