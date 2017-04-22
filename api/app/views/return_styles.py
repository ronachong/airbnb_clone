class ListStyle(object):
    @staticmethod
    def list(select, request):
        # select is a selection of resource like User.select()
        # request is a request object

        page_no = int(request.args.get('page', 1))
        results_per_page = int(request.args.get('number', 10))

        data = []
        end_ind = page_no*results_per_page
        start_ind = end_ind - results_per_page

        print start_ind, end_ind
        for record in select[start_ind:end_ind]:
            data.append(record.to_hash())

        return { 'data': data }
