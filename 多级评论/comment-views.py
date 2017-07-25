def article(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 按照：分类，标签，时间
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))
    # select xxx as x

    obj = models.Article.objects.filter(blog=blog,nid=nid).first()


    # ####################### 评论 #############################
    msg_list = [
        {'id':1,'content':'写的太好了','parent_id':None},
        {'id':2,'content':'你说得对','parent_id':None},
        {'id':3,'content':'顶楼上','parent_id':None},
        {'id':4,'content':'你眼瞎吗','parent_id':1},
        {'id':5,'content':'我看是','parent_id':4},
        {'id':6,'content':'鸡毛','parent_id':2},
        {'id':7,'content':'你是没呀','parent_id':5},
        {'id':8,'content':'惺惺惜惺惺想寻','parent_id':3},
    ]
    msg_list_dict = {}
    for item in msg_list:
        item['child'] = []
        msg_list_dict[item['id']] = item

    # #### msg_list_dict用于查找,msg_list
    result = []
    for item in msg_list:
        pid = item['parent_id']
        if pid:
            msg_list_dict[pid]['child'].append(item)
        else:
            result.append(item)
    # ########################### 打印 ###################
    from utils.comment import comment_tree
    comment_str = comment_tree(result)

    return render(
        request,
        'article.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'obj':obj,
            'comment_str':comment_str
        }
    )
