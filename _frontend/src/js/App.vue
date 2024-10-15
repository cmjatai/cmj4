<script setup>
import Counter from "./Counter.vue"
</script>

<template>
    <h1>{{message}}</h1>
    <counter />
    <ul>
      <li v-for="wsm in wsmessages">
        {{ wsm }}
      </li>
    </ul>

</template>

<script>
export default {
  components: { Counter },
  data() {
    return {
      message: JSON.parse(document.getElementById("vue-message").textContent),
      websocket: null,
      connection_ready: false,
      connection_error: false,
      wsmessages: [],
    }
  },
  methods: {

    onSocketOpen(evt){
      this.connection_ready = true;
    },
    onSocketMessage(evt){
      var received = JSON.parse(evt.data)
      this.wsmessages.push( received.message )
    },

    onSockerError(evt){
      this.connection_error = true;
    },

  },
  mounted() {
    console.log('init app')
    //connect to Sockets
    let sockets_url = (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/time-refresh/'
    this.websocket = new WebSocket(sockets_url)

    this.websocket.onopen    = this.onSocketOpen;
    this.websocket.onmessage = this.onSocketMessage;
    this.websocket.onerror   = this.onSockerError;
  }
}
</script>