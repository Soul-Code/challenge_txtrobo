<template>
  <transition name="slide">
    <div class="chatroom">
      <div class="back">
        <span class="dissname">聊天机器人</span>
      </div>
      <div class="content">
        <div class="content-wrapper" ref="xwBody">
          <div class="content-text" >
            <!--            <div class="content-top">-->
            <!--              <p>————现在可以和我聊天了————</p>-->
            <!--            </div>-->
            <div class="content-body" ref="body">
              <ul class="inHtml" :key="item" v-for="item in content">
                <li class="ask" v-show="item.askContent">
                  <img :src="item.askImg">
                  <p>{{item.askContent}}</p>
                </li>
                <li class="reply" v-show="item.replyContent">
                  <img :src="item.replyImg">
                  <p v-html="item.replyContent"></p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="bottom">
        <div class="send">
          <input v-on:keyup.enter="sendContent" type="text" placeholder="请输入聊天内容" class="sText" ref="sTest">
          <input type="button" class="btn" value="发送" @click="sendContent">
        </div>
      </div>
      <router-view></router-view>
    </div>
  </transition>
</template>

<script type="text/ecmascript-6">
  import BScroll from "better-scroll";

  import {mapGetters} from "vuex";

  export default {
    components: {
      BScroll
    },
    props: {
      probeType: {
        type: Number,
        default: 1
      },
      click: {
        type: Boolean,
        default: true
      },
      data: {
        type: Array,
        default: null
      },
    },
    data() {
      return {
        text: "",
        content: [
          // {
          //   askImg: require('../../assets/me/minion.png'),
          //   replyImg: '',
          //   askContent: '你好',
          //   replyContent: '谢谢'
          // },
          // {
          //   askImg: require('../../assets/me/minion.png'),
          //   replyImg: '',
          //   askContent: '你是谁',
          //   replyContent: '你猜啊'
          // }
        ]
      };
    },
    computed: {
      ...mapGetters(["info"])
    },
    created() {
    },
    mounted() {
      // this.$nextTick(() => {
      //   if (!this.scroll) {
      //     this.scroll = new BScroll(this.$refs.xwBody, {
      //       click: true,
      //       scrollY:true
      //     });
      //   } else if (!this.$refs.xwBody) {
      //     return;
      //   } else {
      //     this.scroll.refresh();
      //   }
      // });
    },
    methods: {
      back() {
        this.$router.back(); // 返回上一级
      },
      sendContent() {
        this.text = this.$refs.sTest.value;
        if (this.text !== "") {
          this.content.push({
            askImg: require("../assets/me/minion.png"),
            askContent: this.text
          });

          var postdata = {};
          postdata.txt = this.text;
          this.$axios
            .post("http://soulcode.cn:8080/txtrobo/api/chat", postdata)
            .then(res => {
              console.log(res.data.answer);
              this.content.push({
                replyImg: "",
                replyContent: res.data.answer
              });
              for (let i = 0; i < this.content.length; i++) {
                // 定义回复者的头像
                this.content[i].replyImg =
                  "http://static.bbs.9wee.com/attachment/forum/201306/07/210751qbp4p4c5yzhhbpym.jpg";
              }
            })
            // 错误处理
            .catch(error => {
              console.log(error);
            });
          this.scrollToBottom();
        }
        this.$refs.sTest.value = ""; // 清空输入框的内容
      },
      clearContent() {
        this.content = [];
      },
      scrollToBottom() {
        // setTimeout(() => {
        //   // 滚动条长度
        //   var currentDistance =
        //     this.$refs.xwBody.scrollHeight - this.$refs.xwBody.clientHeight;
        //   console.log(currentDistance);
        //   // 当前滚动条距离顶部的距离
        //   var currentScrollY = this.$refs.xwBody.scrollTop;
        //   if (currentDistance > 0 && currentDistance > currentScrollY) {
        //     currentScrollY =
        //       Math.ceil((currentDistance - currentScrollY) / 10) + currentScrollY;
        //     currentScrollY =
        //       currentScrollY > currentDistance ? currentDistance : currentScrollY;
        //     // 微信和qq浏览器不支持 scrollTo？
        //     this.$refs.xwBody.scrollTo(0, currentScrollY);
        //     this.$refs.xwBody.scrollTop = currentScrollY;
        //     this.scrollToBottom();
        //   }
        // }, 13);
        setTimeout(() => {
          this.$refs.xwBody.scrollTop = this.$refs.xwBody.scrollHeight
          // 滚轮便宜位置下移
          this.scrollToBottom() //再做一次 避免只是下移了我方增加的对话框
        },13) // 避免下移到倒数第二个对话框
      }
    }
  };
</script>

<style scoped>
  .chatroom {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 19;
    background-color: #ffffff;
  }

  .back {
    background: #ededed;
    height: 50px;
    color: #000000;
    position: fixed;
    width: 100%;
    text-align: center;
    /*padding-left: 44%;*/
  }

  .back .img {
    position: absolute;
    top: 25px;
    margin-top: -8px;
  }

  .back .dissname {
    position: relative;
    font-size: 20px;
    top: 15px;

    /*text-align: center;*/
    /*border-left: 1px solid #000;*/
  }

  .back .logo {
    position: absolute;
    font-size: 20px;
    top: 30px;
    margin-top: -15px;
    right: 20px;
  }

  .content {

    position: fixed;
    top: 50px;
    bottom: 50px;
    left: 0;
    right: 0;
    /*border: 1px solid red;*/
  }

  .content-wrapper {
    background: url("http://soulcode.cn/static/txtrobo/img/bkgrd.png") center center ;
    height: 100%;
    background-size:cover;

    overflow: hidden;
  }

  .content-top {
    font-size: 14px;
    color: rgba(153, 153, 153, 0.6);
    text-align: center;
    margin-top: 4px;
  }

  .content-body {

    position: relative;
    padding: 20px 10px;
    /*overflow: hidden;*/
    /*border: 1px solid blue;*/
  }

  .content-body li {
    position: relative;
    overflow: hidden;
    margin-bottom: 15px;
    line-height: 28px;
  }

  .inHtml img {
    position: relative;
    width: 30px;
    height: 30px;
  }

  .inHtml {
    padding: 0;
  }

  .ask {
    text-align: right;
  }

  .reply {
    text-align: left;
  }

  .ask img {
    float: right;
    margin-left: 15px;
  }

  .reply img {
    float: left;
    margin-right: 15px;
  }

  .reply p,
  .ask p {
    border-radius: 4px;
    text-align: left;
    font: 14px "Microsoft YaHei";
    line-height: 30px;
  }

  .ask p {
    float: right;
    padding: 3px 10px;
    max-width: 182px;
    background: #08c261;
    color: #fff;
  }

  .reply p {
    left: 2pc;
    float: left;
    padding: 3px 10px;
    max-width: 190px;
    background: #ededed;
  }

  .bottom {
    position: fixed;
    height: 50px;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #ededed;
  }

  .send {
    display: flex;
    background-color: #ededed;
  }

  .sText {
    flex: 6;
    height: 30px;
    margin: 10px;
    border: 0;
    padding-left: 8px;
    font-size: 15px;
  }

  .sText.active {
    background-color: red;
  }

  .btn {
    flex: 1;
    width: 65px;
    height: 30px;
    margin: 10px 10px;
    border: 0;
    border-radius: 5px;
    /*float: right;*/
    text-align: center;
    font-size: 14px;
    color: white;
    background-color: #08c261;
  }
</style>
