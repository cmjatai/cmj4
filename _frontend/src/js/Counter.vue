<template>
    <button @click="clickCount">{{count}}</button>
    <div v-html="jresponse"></div>
</template>

<script>
export default {
  data() {
    return {
      count: JSON.parse(document.getElementById("initial-value").textContent),
      jresponse: ''
    }
  },
  methods: {
    clickCount() {
      this.count++


    fetch('http://localhost:9000/teste')
      .then(response => response.json())
      .then(data => {
        this.jresponse = `${data.id} - ${data.teste}`
      })

    }
  }
};
</script>