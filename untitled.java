package graph;

/* See restrictions in Graph.java. */

import java.util.*;

/** Implements a generalized traversal of a graph.  At any given time,
*  there is a particular collection of un-traversed vertices---the "fringe."
*  Traversal consists of repeatedly removing an un-traversed vertex
*  from the fringe, visiting it, and then adding its un-traversed
*  successors to the fringe.
*
*  Generally, the client will extend Traversal.  By overriding the visit
*  method, the client can determine what happens when a node is visited.
*  By supplying an appropriate type of Queue object to the constructor,
*  the client can control the behavior of the fringe. By overriding the
*  shouldPostVisit and postVisit methods, the client can arrange for
*  post-visits of a node (as in depth-first search).  By overriding
*  the reverseSuccessors and processSuccessor methods, the client can control
*  the addition of neighbor vertices to the fringe when a vertex is visited.
*
*  Traversals may be interrupted or restarted, remembering the previously
*  marked vertices.
*  @author Ahmad Badary
*/
public abstract class Traversal {

/** A Traversal of G, using FRINGE as the fringe. */
protected Traversal(Graph G, Queue<Integer> fringe) {
    _G = G;
    _fringe = fringe;
    marked = new ArrayList<>(_G.)
}

/** Unmark all vertices in the graph. */
public void clear() {
    // FIXME
}

/** Initialize the fringe to V0 and perform a traversal. */
public void traverse(Collection<Integer> V0) {
    // FIXME
    _fringe.clear();
    _fringe.addAll(V0);
    while (!_fringe.isEmpty()) 
    {
        int to_visit = _fringe.remove();
        if (to_visit < 0) {
            postVisit(-to_visit);
        } else if (!marked(to_visit)) {
            mark(to_visit);
            if (!visit(to_visit)) {
                return;
            }
            if (shouldPostVisit(to_visit)) {
                if (reverseSuccessors(to_visit)) {
                    _fringe.add(-to_visit);
                }
            }
            if (reverseSuccessors(to_visit)) {
                int m;
                for (int j = _G.outDegree(i) - 1; j >= 0; j--)
          {
            m = _G.successor(i, j);
            if (processSuccessor(i, m)) {
              _fringe.add(Integer.valueOf(m));
            }
          }
                }
            } else {
                Iteration<Integer> iterEdges = _G.successors(to_visit);
                while (iterEdges.hasNext()) {
                    int toVisit = iterEdges.next();
                    boolean doAdd = processSuccessor(to_visit, toVisit);
                    if (doAdd) {
                        _fringe.add(toVisit);
                    }
                }
                if (shouldPostVisit(to_visit)) {
                    _fringe.add(-to_visit);
                }
            }
        } else {
            continue;
        }
    }
}

/** Initialize the fringe to { V0 } and perform a traversal. */
public void traverse(int v0) {
    traverse(Arrays.<Integer>asList(v0));
}

/** Returns true iff V has been marked. */
protected boolean marked(int v) {
    // FIXME
//        System.out.println("vertex = " + v);
    return marked.get(v - 1);
}

/** Mark vertex V. */
protected void mark(int v) {
    // FIXME
    marked.set(v - 1, true);
}

/** Perform a visit on vertex V.  Returns false iff the traversal is to
 *  terminate immediately. */
protected boolean visit(int v) {
    return true;
}

/** Return true if we should postVisit V after traversing its
 *  successors.  (Post-visiting generally is useful only for depth-first
 *  traversals, although we define it for all traversals.) */
protected boolean shouldPostVisit(int v) {
    return false;
}

/** Revisit vertex V after traversing its successors.  Returns false iff
 *  the traversal is to terminate immediately. */
protected boolean postVisit(int v) {
    return true;
}

/** Return true if we should schedule successors of V in reverse order. */
protected boolean reverseSuccessors(int v) {
    return false;
}

/** Process successor V to U.  Returns true iff V is then to
 *  be added to the fringe.  By default, returns true iff V is unmarked. */
protected boolean processSuccessor(int u, int v) {
    return !marked(v);
}

/** The graph being traversed. */
private final Graph _G;
/** The fringe. */
protected final Queue<Integer> _fringe;
// FIXME
protected ArrayList<Boolean> marked;

}
