<template>
  <div id="app">
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {}
};
</script>

<style>
body {
  line-height: 1;
  font-family: "Avenir Next", "Lantinghei SC";
  font-smoothing: antialiased; /*字体平滑显示*/
}
</style>
